from retrieve_paper_bmc import retrieve_bmc_paper
from create_notebook_selenium import create_notebooklm

if __name__ == "__main__":
    print("Retrieving this week's paper...")
    weekly_paper = retrieve_bmc_paper()
    print(f"Paper retrieved with url: {weekly_paper}\n\n")
    print("Creating NotebookLM...\n")
    create_notebooklm(weekly_paper)