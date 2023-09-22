"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import sql, secretmanager, cloudrun, iam
import pulumi_gcp as gcp

#define variable
region_local = "northamerica-northeast1"
project_local = "phx-01h28kjpmp42v8xh59v0qvfpxa"
#docker image of dhis2
docker_image = "dhis2/core:2.39.1.2"
# TODO: save password as secret
password = "mypassword"

# Create a secret for the database password
# db_password_secret = secretmanager.Secret("my-db-password",
#     secret_id="db-password",
#     replication=secretmanager.SecretReplicationArgs(
#         automatic=secretmanager.SecretReplicationAutomaticArgs(),
#     ),
# )

# Create a secret version for the latest database password
# secret_version = secretmanager.SecretVersion("my-db-password-version",
#     secret=db_password_secret.id,
#     secret_data=pulumi.Output.secret("YourDatabasePassword"),
# )

# Create a Cloud SQL instance
instance = sql.DatabaseInstance(
    "dhis2-instance",
    database_version="POSTGRES_12",
    region = region_local,
    settings=sql.DatabaseInstanceSettingsArgs(
        tier="db-f1-micro",
    ),
    deletion_protection=False
)

# Create a database in the Cloud SQL instance
database = sql.Database("dhis-db",
    instance=instance.name,
    name="DHIS2_db",
    project = project_local,
)

# create db admin
user = sql.User("user",
                name="admin",
                instance=instance.name,
                password=password)


# cloud run to deploy dhis2 docker image, with connection to cloud database becuase cloud run is stateless
service = cloudrun.Service('dhis2-service', 
    location=region_local,
    template=cloudrun.ServiceTemplateArgs(
        spec=cloudrun.ServiceTemplateSpecArgs(
            containers=[cloudrun.ServiceTemplateSpecContainerArgs(
                image=docker_image,
                envs=[
                    cloudrun.ServiceTemplateSpecContainerEnvArgs(
                        name='DATABASE_USER',
                        value= user.name, # Specify your database username here
                    ),
                    cloudrun.ServiceTemplateSpecContainerEnvArgs(
                            name="DB_HOST",
                            value= instance.connection_name, # Specify database host
                        ),
                    cloudrun.ServiceTemplateSpecContainerEnvArgs(
                        name='DATABASE_NAME',
                        value= database.name , # Specify your database name here
                    ),
                    cloudrun.ServiceTemplateSpecContainerEnvArgs(
                        name='DATABASE_PASSWORD',
                        value= user.password, # Specify your database password here
                    ),
                ],
            )],
        )),
    traffics=[cloudrun.ServiceTrafficArgs(
        latest_revision=True,
        percent=100,
    )],
)

# set allow-unauthenticated user access
noauth_iam_policy = gcp.organizations.get_iam_policy(bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
    role="roles/run.invoker",
    members=["allUsers"],
)])
noauth_iam_policy = gcp.cloudrun.IamPolicy("noauthIamPolicy",
    location=service.location,
    project=service.project,
    service=service.name,
    policy_data=noauth_iam_policy.policy_data)

# Export the Cloud SQL instance connection name and database name
pulumi.export("database_name", database.name)
pulumi.export("instance_connection_name", instance.connection_name)
pulumi.export("service", service.statuses)
pulumi.export("service_url", service.statuses[0].url)
