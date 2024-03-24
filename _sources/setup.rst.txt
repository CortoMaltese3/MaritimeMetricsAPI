Setup and Running
=================

For Developers
--------------

1. **Clone the Repository**:

   .. code-block:: sh

      git clone https://github.com/CortoMaltese3/MaritimeMetricsAPI.git
      cd MaritimeMetricsAPI
      git checkout main

2. **Set Up a Virtual Environment** (optional but recommended):

   .. code-block:: sh

      # Using venv
      python -m venv venv
      source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

      # Or using Conda
      conda create --name maritime python=3.8
      conda activate maritime

3. **Install Dependencies**:

   .. code-block:: sh

      pip install -r requirements.txt

4. **Create a `.env` File** based on the `.env.template` in the root directory.

5. **Start the Flask Application Locally**:

   .. code-block:: sh

      flask run

For Production
--------------

1. **Ensure Docker and Docker-Compose are Installed**:

   - `Install Docker <https://docs.docker.com/get-docker/>`_
   - `Install Docker Compose <https://docs.docker.com/compose/install/>`_

2. Follow steps 1 to 4 from the Developers section.

3. **Use Docker Compose to Run the Application**:

   .. code-block:: sh

      docker-compose up --build
