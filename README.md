# python-function-custom
Example of how to build and deploy a Python based Azure Function with custom dependencies.

# The steps:

Created the Azure function app as usual – python app with a consumption plan called davpo-demo-python. 

Using WSL I created a folder called __python-function-custom__ (this folder)

Make sure you have all the usual pre-requisites installed, outlined in the Cofigure Your Environment here (az cli, python 3, function tools etc): https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser#configure-your-local-environment

Then taking it step by step through function creation:

* cd into the top level python-function-custom directory
```
cd python-function-custom
```
* Create virtual env: 
```
python -m venv .venv
```
* Activate venv:
```
source .venv/bin/activate
```

* Initialise the function project
```
func init MyFunctionProject --python
```

* Copy my custom package WHL file to a local folder for later installation
```
mkdir custom-modules
cp ../packaging/dist/example_pkg_davpo-0.0.1-py3-none-any.whl custom-modules
```

* install custom module into local Python environment
```
pip install custom-modules/example_pkg_davpo-0.0.1-py3-none-any.whl
```

* at this point I can use the custom module in the local function environment, but it won't be deployed up to Azure

* CD into the functions project folder and create a new "HttpExample" function
```
cd MyFunctionProject
func new --name HttpExample --template "HTTP trigger" --authlevel "anonymous"
```

My custom package is really simple and is called davpopackage, with a single module called davpo_module. It contains a single function "return_fortytwo()"
that returns the number 42.

Now if I update the function to import the custom module and access the function, I can call "func start" and it will already work without any problems because the custom package is installed into the environment I'm using while I'm executing the function core tools.

Next to add the custom package in a way that can be built and deployed to Azure along with the rest of the function's dependencies...

* cd back up to the top level folder (in my case project-function-custom) and create a requirements.txt file (note this is seperate from the one in the actual MyFunctionProject folder):
```
cd ..
touch requirements.txt
```

* edit the temporary requirements.txt file to include all the dependencies we need building into the deployable artifact, including the WHL file in the 
custom-modules folder:
```
vi requirements.txt
```
* This is what the contents of my file requirements.txt looks like:

```
azure-functions
./custom-modules/example_pkg_davpo-0.0.1-py3-none-any.whl
```

* Now run the command that publishes these dependencies into the folder MyFunctionProject/.python_packages. The location of this folder is key:
```
pip install  --target="MyFunctionProject/.python_packages/lib/site-packages"  -r requirements.txt
```

* Now we are ready to do the deployment with the no-build flag which will deploy the project as-is, including all the project dependencies (in the .python_packages folder). Assuming you are logged in correctly with "az login" and the function app name in Azure is davpo-demo-python:
```
cd MyFunctionProject
func azure functionapp publish davpo-demo-python --no-build
```

__At this point the function should deploy with its dependencies and be executable. The example here calls the "return_fortytwo()" function that exists in the custom package deployed up to Azure.__
