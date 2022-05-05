import configparser
import boto3
import json


def main():
    '''
    Reads configuration file, creates needed references to resources / clients in AWS, deletes Redshift cluster, IAM role, and ingress rule.
    '''
    # Parse the config file
    config = configparser.ConfigParser()
    try:
        config.read_file(open('dwh.cfg'))
    except Exception as e:
        print(e)
        
    # Assign our needed config values
    KEY                    = config.get('AWS','KEY')
    SECRET                 = config.get('AWS','SECRET')
    DWH_CLUSTER_IDENTIFIER = config.get('DWH','DWH_CLUSTER_IDENTIFIER')
    DWH_PORT               = config.get('DWH','DWH_PORT')
    DWH_IAM_ROLE_NAME      = config.get('DWH','DWH_IAM_ROLE_NAME')

    # Create needed resources/clients
    iam = boto3.client('iam',aws_access_key_id=KEY,
                         aws_secret_access_key=SECRET,
                         region_name='us-west-2'
                      )
    
    ec2 = boto3.resource('ec2',
                       region_name="us-west-2",
                       aws_access_key_id=KEY,
                       aws_secret_access_key=SECRET
                    )


    redshift = boto3.client('redshift',
                           region_name="us-west-2",
                           aws_access_key_id=KEY,
                           aws_secret_access_key=SECRET
                           )

    # Delete cluster
    try:
        print('Deleting Redshift cluster. This may take a few minutes to complete.')
        redshift.delete_cluster( ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  SkipFinalClusterSnapshot=True)
        # Wait for the cluster to be deleted successfully
        redshift.get_waiter('cluster_deleted').wait(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)
        print("Cluster deleted")
    except Exception as e:
        print(e)

    # Delete IAM role and policy
    try:
        print('Deleting IAM role')
        iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
        iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
        print("IAM role and policy deleted")
    except Exception as e:
        print(e)
        
    # Delete ingress rights
    try:
        print('Revoking ingress for security group')
        sg = list(ec2.security_groups.all())[0]
        sg.revoke_ingress(GroupName=sg.group_name,
                          CidrIp='0.0.0.0/0',
                          IpProtocol='tcp',
                          FromPort=int(DWH_PORT),
                          ToPort=int(DWH_PORT))
        print('Ingress rights revoked')
    except Exception as e:
        print(e)

    print('All resources deleted.')

if __name__ == "__main__":
    main()