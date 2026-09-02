from datetime import timedelta
from langchain_google_community.gmail.utils import build_resource_service
from langchain_google_community import GmailToolkit
from gmail.gmail_auth import obtain_credentials
from gmail.gmail_decoder import decoder_content, clean_all_links


# l'underscore avant le nom de fonction car c'est une fonction interne 
# on appelle que les 2 autres fonctions qui utilisent cette fonction mais jamais celle-ci directement

def _rechercher_mails(query: str):
    credentials = obtain_credentials()
    api_resource = build_resource_service(credentials=credentials)
    toolkit = GmailToolkit(api_resource=api_resource)

    tools = toolkit.get_tools()

    tool_search = None
    for tool in tools:
        if tool.name == "search_gmail":
            tool_search = tool

    research_list_result = tool_search.invoke(
        {
            "query": query,
            "max_results": 50
        }
    )

    mails_non_lus = []
    for mail in research_list_result:
        mails_non_lus.append({
            "objet_mail": decoder_content(mail["subject"]),
            "expediteur": mail["sender"],
            "contenu_mail": clean_all_links(mail["body"]),
            "mail_id": mail["id"]
        })

    return mails_non_lus


def get_unread_emails(nb_jours: int):
    query = f"is:unread newer_than:{nb_jours}d"
    return _rechercher_mails(query)


def get_unread_emails_par_date(date_cible):
    date_suivante = date_cible + timedelta(days=1)
    query = f"is:unread after:{date_cible.strftime('%Y/%m/%d')} before:{date_suivante.strftime('%Y/%m/%d')}"
    return _rechercher_mails(query)