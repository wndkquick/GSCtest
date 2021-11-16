import searchconsole
import streamlit as st

from apiclient import discovery
from google_auth_oauthlib.flow import Flow

#region Layout size ####################################################################################

def _max_width_():
    max_width_str = f"max-width: 1300px;"
    #max_width_str = f"max-width: 1550px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

_max_width_()


st.title("Google OAuth2 flow")
st.header("Load credentials")

st.markdown("Alternatively a user could upload a file with their credentials and you could use `Flow.from_client_secrets_file`")

# Alternatively a user could upload a file with their credentials and you
# could use `Flow.from_client_secrets_file`.

st.markdown(" Client ID _____ ")
st.markdown("Client secret _____ ")
st.write("https://www.tatielou.co.uk/")


st.markdown('## **① Add credentials **') #########

with st.beta_expander("ℹ️ - About this app ", expanded=False):
  st.write("""
	    
-   StreamEA leverages the power of [Google Natural Language API](https://cloud.google.com/natural-language/docs/basics#entity_analysis) to extract entities from web pages!
-   It also highlights missing entities between pages

	    """)
      
  st.markdown("")


#c1, c2, c3, c4 = st.beta_columns(4)
c1, c2, c3 = st.beta_columns(3)

with c1:
    client_id = st.text_input("Client ID", "_______.apps.googleusercontent.com")
  
with c2:
  
    client_secret = st.text_input("Client secret","_______________")

with c3:

    webproperty_box = st.text_input("Web property","https://www.tatielou.co.uk/")

credentials = {
    "installed": {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uris": [],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token"
    }
}
flow = Flow.from_client_config(
    credentials,
    scopes=['https://www.googleapis.com/auth/webmasters.readonly'],
    #redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'    
)


auth_url, _ = flow.authorization_url(prompt='consent')

#myvariable = 4
#mystring = str(myvariable)  # '4'

#st.write(auth_url)
#st.write(type(auth_url))
#st.markdown(auth_url)
#st.success(auth_url)
#st.markdown("[Click on link](auth_url)")

st.markdown('## ** Paste URL in a new browser window **') #########
#st.markdown('## ** Paste authorisation token **') #########

c4, c5, c6, c7 = st.beta_columns(4)

with c4:
    #client_id = st.text_input("Client ID")
    #st.text("")
    #st.text("")
    st.write(auth_url)
    #st.code(auth_url)
  
with c6:  
    text = st.text_input("add arrow","add arrow/image" )
    #client_secret = st.text_input("Client secret")

with c7:  
    code = st.text_input('Code')
    #client_secret = st.text_input("Client secret")



try:
    flow.fetch_token(code=code)

    credentials = flow.credentials
    st.write(credentials)
    st.write("credentials type")
    st.write(type(credentials))


    service = discovery.build(
        serviceName='webmasters',
        version='v3',
        credentials=credentials,
        #Original Value
        cache_discovery=False,
        #Test Value
        #cache_discovery=True,
    )

    st.write(service)

    '''
    import json

    try:
        with open("credentials.json", "r") as f:
            my_dict = json.load(f)

        st.header("2nd JSON file: credentials.json")
        st.write(my_dict)
    except FileNotFoundError:
        st.warning('credentials.json NOT THERE')
    '''

    account = searchconsole.account.Account(service, credentials)

    #account = searchconsole.account.Account(service, credentials, serialize='credentials.json')

    st.write(service)


    #@st.cache()
    #def accountSetUp():
    #    searchconsole.account.Account(service, credentials)
    #account = accountSetUp()

    ###############
    #account = searchconsole.authenticate(client_config='client_secrets.json')
    #webproperty = account['https://www.example.com/']
    #webproperty = account['https://www.tatielou.co.uk/']

    st.write('## Flow from Josh **') #########

    webproperty = account[webproperty_box]
    report = webproperty.query.range('today', days=-7).dimension('query').get()
    st.write(report.rows)
    st.write(type(report.rows))


    #st.stop()

    st.write('## Flow from RanSense **') #########

    #let's build a pandas dataframe with the search console data
    import pandas as pd

    def get_search_console_data(webproperty, days=-365):
        if webproperty is not None:
            query = webproperty.query.range(start='today', days=days).dimension('date')
            r = query.get()
            df = pd.DataFrame(r.rows)
            return df

        print("Web property doesn't exist, please select a valid one from this list")
        print(account.webproperties)

        return None

    df = get_search_console_data(webproperty)

    st.write(df.info())
    st.write(df)

    dfSaved = df.to_csv('test.csv')
    #dfNew = pd.read_csv('/content/test.csv')

except:
    pass


import pandas as pd

try:
    dfNew = pd.read_csv('test.csv')
    st.write("dfSaved.head()")
    st.write(dfNew.head())
except FileNotFoundError:
    st.warning("fill in credentials 1st")


agree = st.checkbox('I agree')

if agree:
    st.write('Great!')


st.stop()

dft = df[['date','clicks']]

dft = dft.rename(columns={"date":"ds", "clicks":"y"})

dft.info()
