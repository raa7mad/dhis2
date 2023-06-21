"""A Google Cloud Python Pulumi program"""

import pulumi
from pulumi_gcp import sql, secretmanager

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
    region="northamerica-northeast1",
    settings=sql.DatabaseInstanceSettingsArgs(
        tier="db-f1-micro",
    ),
    deletion_protection=False
)

# Create a database in the Cloud SQL instance
database = sql.Database("dhis-db",
    instance=instance.name,
    name="DHIS2_db"
)

# Export the Cloud SQL instance connection name and database name
pulumi.export("instance_connection_name", instance.connection_name)
pulumi.export("database_name", database.name)