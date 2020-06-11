# foodbot

REQUIREMENTS: Python 3, NLTK, Flask, ngrok

To run the project, clone this repo.  
In project directory, mkdir pickled_files.  
Fire up Python3, run an instance of object from NaiveBayes.  
Run the train() and store_pickle() methods of NaiveBayes.  
OR, check and run train.py.

Make sure Dialogflow is set up correctly for use.
Make an account and sign-in to Dialogflow, create a new agent.

Go to Agent Settings (cog wheel next to agent name) > Export and Import > select Restore from ZIP.

Upload the included dialogflow_intents.zip.  

Run foodbot.py.  

Set up an ngrok tunnel to localhost.
Run the following command (worked for Hongchao, failed for Ajay): 
    ngrok http 5000  
If you have weird issues, run the following (fixed for Ajay):
    ngrok http 127.0.0.1:5000 -host-header="127.0.0.1:5000"   

Copy the https fowarding URL.

Go to Dialogflow > Fulfillment.
Under URL, paste the URL from ngrok AND append "/webhook".  
    Example: https://randomgenurl.ngrok.io/webhook  

The application can now be tested in the Dialogflow Fulfillment Test Console to the left of the URL field, or for a nicer view go to Integrations, scroll down to Text Based, turn on the Web Demo, click on it and follow the URL.


