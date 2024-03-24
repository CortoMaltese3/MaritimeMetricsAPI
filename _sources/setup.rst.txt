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


API Testing with Swagger UI
---------------------------

MarineMetricsAPI includes a Swagger UI interface that allows developers and users to interactively test the API endpoints without writing any code. The Swagger UI provides a web-based interface where you can see all available API endpoints, their required parameters, and even execute API calls directly from your browser.

To access the Swagger UI:

1. Ensure the Flask application is running. If it's not, start the Flask server by running:

   .. code-block:: sh

      flask run

   Or, if you're using Docker:

   .. code-block:: sh

      docker-compose up --build

2. Open your web browser and navigate to `/apidocs` on your Flask server's address. If you're running the server locally, the Swagger UI will typically be available at:

   `http://localhost:5000/apidocs`

3. Explore the API endpoints listed in the Swagger UI. You can expand each endpoint to see detailed information about the request parameters, expected responses, and even try out the endpoint directly by clicking on the "Try it out" button, entering the required parameters, and observing the API response.
