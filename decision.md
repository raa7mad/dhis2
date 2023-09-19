Hosting DHIS2 on GCP

# options to install DHIS2

## requirement
recommends Ubuntu 18.04 LTS operating system, PostgreSQL database system and Tomcat Servlet container as the preferred environment for server installations.

### server specification
RAM: At least 2 GB for a small instance, 12 GB for a medium instance, 64 GB or more for a large instance.

CPU cores: 4 CPU cores for a small instance, 8 CPU cores for a medium instance, 16 CPU cores or more for a large instance.

Disk: SSD is recommeded as storage device. Minimum read speed is 150 Mb/s, 200 Mb/s is good, 350 Mb/s or better is ideal. At least 100 GB storage space is recommended, but will depend entirely on the amount of data which is contained in the data value tables. Analytics tables require a significant amount of storage space. Plan ahead and ensure that your server can be upgraded with more disk space as needed.

### Software requirements
An operating system for which a Java JDK or JRE version 8 or 11 exists. Linux is recommended.
Java JDK. OpenJDK is recommended.
For DHIS 2 version 2.38 and later, JDK 11 is required.
For DHIS 2 version 2.35 and later, JDK 11 is recommended and JDK 8 or later is required.
For DHIS 2 versions older than 2.35, JDK 8 is required.
PostgreSQL database version 9.6 or later. A later PostgreSQL version such as version 14 is recommended.
PostGIS database extension version 2.2 or later.
Tomcat servlet container version 8.5.50 or later, or other Servlet API 3.1 compliant servlet containers.
Cluster setup only (optional): Redis data store version 4 or later.

## installation methods
1. **Manual Installation:**
   - Manually installing DHIS2 involves downloading the DHIS2 WAR file from the official DHIS2 website (https://www.dhis2.org/downloads) and deploying it to your server.
   - You'll need to set up a database (e.g., PostgreSQL) separately, configure it, and connect DHIS2 to it.
   - This option provides maximum control but may require more technical expertise.

2. **Docker Installation:** (container solution)
   - You can use Docker to run DHIS2 in a containerized environment. Docker provides a consistent and isolated environment for DHIS2 and its dependencies.
   - DHIS2 Docker images are available, making it easier to set up and deploy DHIS2 in a container.
   - Docker is a popular choice for development, testing, and deployment in various environments.

3. **Docker Compose:** (container solution)
   - Docker Compose is a tool for defining and running multi-container Docker applications. DHIS2 can be set up in conjunction with a database (e.g., PostgreSQL) using a `docker-compose.yml` configuration file.
   - Docker Compose simplifies the setup of interconnected containers, making it suitable for local development and small-scale deployments.                      

7. **Container Orchestration (Kubernetes):** (container solution)
   - You can deploy DHIS2 in a containerized environment using container orchestration platforms like Kubernetes.
   - Kubernetes offers scalability, high availability, and automated management of DHIS2 containers.

8. **Package Managers (Community Edition):**
   - Some Linux distributions include DHIS2 packages that can be installed using package managers like apt (Debian/Ubuntu) or yum (Red Hat/CentOS). This is typically suitable for the DHIS2 Community Edition.

9. **Virtual Appliances (Community Edition):**
   - Virtual appliances are pre-configured, ready-to-use DHIS2 images that can be deployed on virtualization platforms like VMware or VirtualBox. These are typically available for the DHIS2 Community Edition.

10. **DHIS2 Hosting Providers:**
    - Some organizations and hosting providers offer managed DHIS2 hosting services, where they take care of the installation, maintenance, and infrastructure management on your behalf.

The choice of installation method depends on factors such as your technical expertise, infrastructure preferences, scalability requirements, and whether you want to manage the installation yourself or prefer a managed solution. Be sure to refer to the DHIS2 documentation for detailed installation instructions for your chosen method, as the specifics can vary based on the approach you select.
