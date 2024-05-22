import streamlit as st


st.set_page_config(page_title="DGA Detector", 
                   page_icon="👋", 
                   layout="centered")

st.write("# Domain Generation Algorithms (DGAs)")

st.markdown(
    """
    In the realm of cybersecurity, one of the sophisticated methods used by cybercriminals to evade detection and maintain control over 
    their malicious infrastructure is through Domain Generation Algorithms (DGAs). To understand the impact and function of DGAs, 
    it's essential to first grasp the basics of the Domain Name System (DNS) protocol.

    The DNS protocol is a cornerstone of the internet, responsible for translating human-readable domain names like _:blue[example.com]_ into IP addresses 
    that computers use to identify each other on the network. When you type a web address into your browser, a DNS query is made to a DNS server 
    to fetch the corresponding IP address, enabling your browser to connect to the correct web server.
    """
)

st.image('C:/Users/Jorge Payà/Desktop/4Geeks/Final Project/Code/DGA-Detection-final/src/img/dnsprotocol.png')

st.markdown("""
    #### What is a DGA?
    A Domain Generation Algorithm (DGA) is a technique used by malware to periodically generate a large number of domain names that 
    can be used as rendezvous points with their command-and-control (C&C) servers. Instead of using a fixed set of domain names that can be easily 
    blocked or taken down by defenders, DGAs create a virtually infinite pool of domain names, making it significantly harder for cybersecurity measures 
    to disrupt the malware’s communication channels.
   
    #### How DGA Attacks Work
    - :red[Infection]: A computer or device gets infected with malware that includes a DGA.
    - :red[Domain Generation]: The DGA within the malware generates a new list of domain names based on specific algorithms and time-based parameters.
    - :red[DNS Queries]: The infected device makes DNS queries to resolve these generated domain names, attempting to connect to the C&C server.
    - :red[Successful Connection]: If one of these domains resolves to an IP address controlled by the attacker, the malware establishes a connection to the 
    C&C server, allowing the attacker to issue commands, steal data, or update the malware.
    
    #### The Challenge for Defenders
    Traditional DNS filtering and blocking techniques struggle against DGA-based attacks because of the dynamic nature of the generated domain names. 
    Security teams must employ advanced machine learning models to detect and classify DGA-generated domain names from legitimate ones. 
    These models analyze patterns, linguistic features, and query behaviors to effectively identify and mitigate the threat posed by DGAs.
    
"""
)
