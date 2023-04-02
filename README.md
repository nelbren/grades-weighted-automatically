# Grades weighted automatically using API of Canvas Instructure

![](grades-weighted-automatically.jpg)


1. ## Get your API_KEY like this:
   - Canvas->Account->Settings->New Access Token->Fill fields of Purpose and Expires->Generate token->Copy the token!
   - Or view this video: https://www.youtube.com/watch?v=cZ5cn8stjM0

2. ## Install this project

   `git clone https://github.com/nelbren/grades-weighted-automatically.git`

3. ## Install requirements

   - ### Install **Python 3**:
     - #### 🐧Linux
       `sudo apt install python3-pip`
     - #### 🍎 Mac
        [Python Releases for macOS](https://www.python.org/downloads/macos/)
     - #### 🪟 Windows
        **Microsoft Store**->Python 3.10
    - ### Install the necessary **python packages**:
      - #### 🐧Linux, 🍎 Mac or 🪟 Windows
        `install_requirements.bash.bat`

4. ## Set your Instructure URL and API_KEY like this:

   - ### Using the environment variables:
     - #### Rename the **my_set_env** file:
       - ##### 🐧Linux or 🍎 Mac
          Rename **my_set_env.bash.example** to **my_set_env.bash**
       - ##### 🪟 Windows
          Rename **my_set_env.bat.example** to **my_set_env.bat**
       - ##### Setting environment variables in the file.
          - **INSTRUCTURE_URL**='https://some.instructure.com'
          - **API_KEY**='your-api-key'
       - ##### Run:
         - ###### 🐧Linux or 🍎 Mac
           `./run.bash`
         - ###### 🪟 Windows
           `run.bat`
   - ### Or using parameters:
     - #### Setting in the command line:
       - ##### **`-u URL`**, **`--instructure_url https://some.instructure.com`**
       - ##### **`-k API_KEY`**, **`--api_key API_KEY`**
     - #### Run:
       - ##### 🐧Linux, 🍎 Mac or 🪟 Windows
         `python3 grades-weighted-automatically.py -u replace-with-your-INFRASTRUCTURE-URL -k replace-with-your-KEY_API`
