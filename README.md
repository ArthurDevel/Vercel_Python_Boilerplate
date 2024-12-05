## Getting Started
### Setting up the project

From this example: https://github.com/vercel/examples/tree/main/python/nextjs-flask

NOTE: the example above used a Release Candidate version of Next.js (or I accidentally installed it), which caused issues. I downgraded to the stable version (18.2.0).

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

- integrate the next.config.js
- integrate package.json (I had to make some changes to the example, see my file)

Then modify package.json to activate the virtual environment before running the flask server:

```bash
{
  "scripts": {
    // ... existing code ...
    "flask-dev": "source venv/bin/activate && FLASK_DEBUG=1 pip install -r requirements.txt && python -m flask --app api/index run -p 5328"
    // ... existing code ...
  }
}
```


To have the flask server reload on code changes, add the `--reload` flag to the `flask-dev` script in package.json. This makes it easier to test changes locally.
```bash
{
  "scripts": {
    "flask-dev": "source venv/bin/activate && FLASK_DEBUG=1 pip install -r requirements.txt && python -m flask --app api/index run -p 5328 --reload"
  }
}
```

*Why did we do this?* We want to be able to test the project locally, AND be able to deploy to Vercel. 

### Running the project on a new local machine
You can skip the previous steps as the project is already set up. 

On your new local machine, create a virtual environment:
```bash
# Navigate to your project directory
cd itempass_alpha

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

Install the dependencies in the virtual environment:
```bash
pip install -r requirements.txt
```

### Testing locally
Use `npm run dev` to run the Next.js app. This should automatically run the flask server too. 

Make sure that the environment variable `NEXT_PUBLIC_API_BASE_URL` is set to `http://localhost:3000`, so your local environment can call the Flask server (remember, we rerouted the API calls to the Flask server in next.config.ts).


### Pushing to Vercel

First, run `npm run build` to check for errors. 
Then, push to Github. Vercel will automatically deploy the new version. 


## Environment Variables
If the environment variable needs to be accessed by the client (browser), it needs to be prefixed with `NEXT_PUBLIC_`. Make sure to set environment variables both in your local .env file, and in the Vercel project settings.


## API Structure V1
*NOTE: this is the old API structure, which we no longer use. It is kept for reference.*

The API needs to be set up in a specific way, such that:
- it works with our production environment on Vercel (so Vercel creates serverless functions)
- it works with our local development environment (so we can test locally with the Flask server)

Our api folder needs to be added to the *root* of the project. 

```
api/
├── index.py                 # Main Flask application entry point
├── hello_world/
│   └── index.py            # Simple blueprint example with hello world endpoint, which can be called with a get request at /api/hello_world
└── lib/
    ├── neo4j_helper.py     # Neo4j database interaction utilities
    └── openai_helper.py    # OpenAI API interaction utilities
```

In the main index.py file, we register the blueprints and define the base route:
```python
from flask import Flask
from other import other_blueprint
from witharguments import witharguments_blueprint

app = Flask(__name__)
app.register_blueprint(hello_world_bp) 
```

Make sure that the blueprints are defined in the index.py file of the function itself. Make sure that the url_prefix matches the folder structure.
```python
from flask import Blueprint
hello_world_bp = Blueprint('hello_world', __name__, url_prefix='/api/hello_world') # we can choose the blueprint name and url_prefix (TO CHECK: does it need to match folder structure?)


@hello_world_bp.route('/get_hello_world', methods=['GET']) # we can choose the api endpoint name
def get_hello_world() -> Dict:
    return handle_get_hello_world()

@hello_world_bp.route('/post_hello_world', methods=['POST']) # we can choose the api endpoint name
def post_hello_world() -> Dict:
    args = request.get_json()
    return handle_post_hello_world(args)
```

When working with arguments (like in the post request above), we created a main function that extracts the arguments from the request, and then calls a handler function with these arguments. This makes it easier to test the function in isolation.

```python
def main():
    args = request.get_json()
    return handle_request(args)

def handle_request(args):
    # Do something with the arguments
    return {"message": "Hello, World!"}
```

### Return format
UITVOGELEN! Dat we hier consistent in zijn

### Calling the API from our frontend
First, create an environment variable `NEXT_PUBLIC_API_BASE_URL` in the .env file, and set it to the base URL of the project (e.g. `http://localhost:3000`). On Vercel, set it to the URL of the project (e.g. `https://itempass-alpha-development.vercel.app` for your development environment, and `https://itempass.com` for production).

To make it easier to work with AI, we separate our API calls into a separate .ts file (eg. `src/app/services/api/hello_world.ts`). As our code-base grows, this keeps the file from becoming too cluttered, which makes it easier for AI to understand.

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

export const helloWorldApi = {
  // Get hello world message
  getHelloWorld: async () => {
    const response = await fetch(`${API_BASE_URL}/api/hello_world/get_hello_world`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    return response.json();
  },

  // Post hello world message with name
  postHelloWorld: async (name: string) => {
    const response = await fetch(`${API_BASE_URL}/api/hello_world/post_hello_world`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    return response.json();
  }
};
```

Now, we can use the API calls in our frontend code.


## Logging Configuration TODO MAKE CONSISTENT AND BETTER, CAN BE SIMPLIFIED
The main index.py file sets up logging for the Flask app. Keep in mind: Vercel has a read-only file system, so we cannot write to files. That's why are detecting VERCEL_ENV to decide whether to log to the console or to a file.

*TODO*: I THINK THIS LOGGING SETUP IS NOT WORKING AS INTENDED. WITH TESTS, A NEW LOGGER IS CREATED

```python
# Configure logging based on environment
if os.environ.get('VERCEL_ENV'):
    # On Vercel, just log to console which will be captured by Vercel's logging system
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )
else:
    # In development, keep file logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('flask_app.log', mode='w')
        ]
    )

# Get the root logger and set its level
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Create a logger specific to your app
logger = logging.getLogger(__name__)

# Add this before request handler to log all requests
@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

# Add this after request handler to log all responses
@app.after_request
def log_response_info(response):
    logger.debug('Response: %s', response.get_data())
    return response

```

In other files, we should not set up logging again, but use the root logger (by calling `logging.getLogger()` without any arguments).

*TODO: test that this works when deployed on Vercel too*

## Configuring Functions: 
### Timeout Configuration
For Flask: When using rewrites in next.config.ts, a default timeout of 30 seconds is set (https://github.com/vercel/next.js/issues/36251). We can override this by adding the following to next.config.js:
```typescript
experimental: {
  proxyTimeout: 60
}
```

This solves the timeout issue for the Flask server. Now, we still need to configure the timeout for our production environment on Vercel. This is done in vercel.json: 

**ISSUE**
Current hypothesis: because we are routing to api/index.py and routing our serverless functions from there, setting the timeout and memory in vercel.json does not work. We can only set these parameters in vercel.json for the api/index.py file itself, and this propagates to all the serverless functions. 

**TO VERIFY**: 
It seems like our development environment is not affected by vercel.json. 

### Memory Configuration
#TODO: probably ignore on local machine, but need to set it up for Vercel. First figure out how to solve the timeout issue for Vercel. 


### Installing on DigitalOcean
Follow this guide: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-22-04
Don't forget to also configure the firewall rules to allow access from your IP address.

To allow connections from any IP (NOT RECOMMENDED):
```bash
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw allow from any to any port 7474 proto tcp
sudo ufw allow from any to any port 7687 proto tcp
sudo ufw reload
```


### Remote access
http://178.128.251.181:7474/browser/ 
http://64.227.79.49:7474/browser/
TODO: security?? It is now protected by a password, would be better to have IP whitelisting added


## RabbitMQ
Just install from template on DigitalOcean. When opening console, you will see the username and password in the output, as well as a link to the web interface.

http://206.189.106.27:15672/



## Debugging
### A Serverless Function has exceeded the unzipped maximum size of 250MB.
Even though the total size of the requirements.txt file is 17MB, the actual size of the serverless function is 250MB+. It seems like other folders/files are being included in the serverless function. 

**DISABLE CACHE**: If cache is your problem (rebuilding from the dashboard works, deploying from git doesn't); add this to environment variable to Vercel: VERCEL_FORCE_NO_BUILD_CACHE=1 (https://vercel.com/docs/deployments/troubleshoot-a-build#managing-build-cache). In my experience, this was a "band-aid" solution, it came back later when my code base grew. 

**EXCLUDE FILES (this was my issue)**: Add this to vercel.json (https://github.com/orgs/vercel/discussions/4354). Make sure to add the excludeFiles parameter to all the serverless functions in the config file:

```json
"functions": {
   "api/**/*.py": {
        "maxDuration": 30,
        "memory": 1024,
        "excludeFiles": "{.next,*.cache,node_modules,public,app}/**"
      }
}
```

For .js api files, other discussion says to add outputFileTraceExcludes to next.config.ts (https://github.com/orgs/vercel/discussions/4354 and https://github.com/orgs/vercel/discussions/103#discussioncomment-6356642)
https://github.com/orgs/vercel/discussions/103#discussioncomment-6676753 

adding .next and .vercel to .gitignore -> didn't solve the issue

## AUTHENTICATION
TODO: how to stay on a page when logging in and logging out, how to properly wrap certain components with authentication

## BUILD TIME
At some point, the build time of the project nears the 45 minute limit.
https://vercel.com/guides/how-do-i-reduce-my-build-time-with-next-js-on-vercel 

TODO: use guide above to reduce build time