"""Read Arxiv Papers."""
import hashlib
import logging
import os
from typing import List, Optional, Tuple

from llama_index import download_loader
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from fpdf import FPDF

class ArxivReader_mod(BaseReader):
    """Arxiv Reader.

    Gets a search query, return a list of Documents of the top corresponding scientific papers on Arxiv.
    """

    def __init__(
            self,
    ):
        """Initialize with parameters."""
        super().__init__()

    def _hacky_hash(self, some_string):
        _hash = hashlib.md5(some_string.encode("utf-8")).hexdigest()
        return _hash

    def load_data(
            self,
            search_query: str,
            papers_dir: Optional[str] = ".papers",
            max_results: Optional[int] = 50,
            search_criterion: Optional[int] = 0,
    ) -> List[Document]:
        """Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

        Args:
            search_query (str): A topic to search for (e.g. "Artificial Intelligence").
            papers_dir (Optional[str]): Locally directory to store the papers
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects.
        """
        # find papers
        import arxiv
        if search_criterion == 0:
            sort_criterion = arxiv.SortCriterion.Relevance

        if search_criterion == 1:
            sort_criterion = arxiv.SortCriterion.LastUpdatedDate

        if search_criterion == 2:
            sort_criterion = arxiv.SortCriterion.SubmittedDate

        arxiv_search = arxiv.Search(
            query=search_query,
            id_list=[],
            max_results=max_results,
            sort_by=sort_criterion,
        )

        search_results = list(arxiv_search.results())
        logging.debug(f"> Successfully fetched {len(search_results)} papers")

        #create directory
        if not os.path.exists(papers_dir):
            os.makedirs(papers_dir)

        paper_lookup = {}
        for paper in search_results:
            # Hash filename to avoid bad charaters in file path
            filename = f"{self._hacky_hash(paper.title)}.pdf"
            #filename = f"{paper.title}.pdf"
            paper_lookup[os.path.join(papers_dir, filename)] = {
                "Title of this paper": paper.title,
                "Authors": (", ").join([a.name for a in paper.authors]),
                "Date published": paper.published.strftime("%m/%d/%Y"),
                "URL": paper.entry_id,
                # "summary": paper.summary
            }
            paper.download_pdf(dirpath=papers_dir, filename=filename)
            logging.debug(f"> Downloading {filename}...")

        def get_paper_metadata(filename):
            return paper_lookup[filename]

        SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
        arxiv_documents = SimpleDirectoryReader(
            papers_dir, file_metadata=get_paper_metadata
        ).load_data()
        # Include extra documents containing the abstracts
        abstract_documents = []
        for paper in search_results:
            d = f"The following is a summary of the paper: {paper.title}\n\nSummary: {paper.summary}"
            abstract_documents.append(Document(d))


        return arxiv_documents + abstract_documents

    def load_papers_and_abstracts(
            self,
            search_query: str,
            papers_dir: Optional[str] = ".papers",
            max_results: Optional[int] = 10,
    ) -> Tuple[List[Document], List[Document]]:
        """Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

        Args:
            search_query (str): A topic to search for (e.g. "Artificial Intelligence").
            papers_dir (Optional[str]): Locally directory to store the papers
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects representing the papers themselves
            List[Document]: A list of Document objects representing abstracts only
        """
        import arxiv

        arxiv_search = arxiv.Search(
            query=search_query,
            id_list=[],
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        search_results = list(arxiv_search.results())
        logging.debug(f"> Successfully fetched {len(search_results)} papers")

        if not os.path.exists(papers_dir):
            os.makedirs(papers_dir)

        paper_lookup = {}
        for paper in search_results:
            # Hash filename to avoid bad charaters in file path
            filename = f"{self._hacky_hash(paper.title)}.pdf"
            paper_lookup[os.path.join(papers_dir, filename)] = {
                "Title of this paper": paper.title,
                "Authors": (", ").join([a.name for a in paper.authors]),
                "Date published": paper.published.strftime("%m/%d/%Y"),
                "URL": paper.entry_id,
                # "summary": paper.summary
            }
            paper.download_pdf(dirpath=papers_dir, filename=filename)
            logging.debug(f"> Downloading {filename}...")

        def get_paper_metadata(filename):
            return paper_lookup[filename]

        SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
        arxiv_documents = SimpleDirectoryReader(
            papers_dir, file_metadata=get_paper_metadata
        ).load_data()
        # Include extra documents containing the abstracts
        abstract_documents = []
        for paper in search_results:
            d = f"The following is a summary of the paper: {paper.title}\n\nSummary: {paper.summary}"
            abstract_documents.append(Document(d))

        # Delete downloaded papers
        try:
            for f in os.listdir(papers_dir):
                os.remove(os.path.join(papers_dir, f))
                logging.debug(f"> Deleted file: {f}")
            os.rmdir(papers_dir)
            logging.debug(f"> Deleted directory: {papers_dir}")
        except OSError:
            print("Unable to delete files or directory")

        return arxiv_documents, abstract_documents

class ArxivReader_mod_search(BaseReader):
    """Arxiv Reader.

    Gets a search query, return a list of Documents of the top corresponding scientific papers on Arxiv.
    """

    def __init__(
            self,
    ):
        """Initialize with parameters."""
        super().__init__()

    def _hacky_hash(self, some_string):
        _hash = hashlib.md5(some_string.encode("utf-8")).hexdigest()
        return _hash

    def load_data(
            self,
            search_query: str,
            papers_dir: Optional[str] = ".papers",
            max_results: Optional[int] = 50,
            search_criterion: Optional[int] = 0,
    ) -> List[Document]:
        """Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

        Args:
            search_query (str): A topic to search for (e.g. "Artificial Intelligence").
            papers_dir (Optional[str]): Locally directory to store the papers
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects.
        """
        #find papers
        import arxiv
        if search_criterion == 0:
            sort_criterion = arxiv.SortCriterion.Relevance

        if search_criterion == 1:
            sort_criterion = arxiv.SortCriterion.LastUpdatedDate

        if search_criterion == 2:
            sort_criterion = arxiv.SortCriterion.SubmittedDate

        arxiv_search = arxiv.Search(
            query=search_query,
            id_list=[],
            max_results=max_results,
            sort_by= sort_criterion,
        )
        search_results = list(arxiv_search.results())
        logging.debug(f"> Successfully fetched {len(search_results)} papers")

        #create directory
        if not os.path.exists(papers_dir):
            os.makedirs(papers_dir)
        else:
            # Delete downloaded papers
            try:
                for f in os.listdir(papers_dir):
                    os.remove(os.path.join(papers_dir, f))
                    logging.debug(f"> Deleted file: {f}")
                os.rmdir(papers_dir)
                logging.debug(f"> Deleted directory: {papers_dir}")
                os.makedirs(papers_dir)
            except OSError:
                print("Unable to delete files or directory")

        paper_lookup = {}
        for paper in search_results:
            # Hash filename to avoid bad charaters in file path
            filename = f"{self._hacky_hash(paper.title)}.pdf"
            #filename = f"{paper.title}.pdf"
            paper_lookup[os.path.join(papers_dir, filename)] = {
                "Title of this paper": paper.title,
                "Authors": (", ").join([a.name for a in paper.authors]),
                "Date published": paper.published.strftime("%m/%d/%Y"),
                "URL": paper.entry_id,
                "summary": paper.summary,
            }

            paper.download_pdf(dirpath=papers_dir, filename=filename)
            logging.debug(f"> Downloading {filename}...")

        def get_paper_metadata(filename):
            return paper_lookup[filename]

        SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
        arxiv_documents = SimpleDirectoryReader(
            papers_dir, file_metadata=get_paper_metadata
        ).load_data()
        # Include extra documents containing the abstracts

        # save FPDF() class into
        # a variable pdf
        pdf = FPDF()

        # Add a page
        pdf.add_page()

        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", size=15)

        # insert the texts in pdf
        for paper in search_results:
            authors = (", ").join([a.name for a in paper.authors])
            pub_paper = paper.published.strftime("%m/%d/%Y")
            d = f"Title: {paper.title}\n\nAuthors:{authors}\n\nDate:{pub_paper}\n\nAbstract: {paper.summary}\n"
            pdf.multi_cell(0, 10, txt= d, border = 0)
            pdf.add_page()


        # save the pdf with name .pdf
        pdf.output(papers_dir+"/abstracts.pdf")





        abstract_documents = []
        for paper in search_results:
            authors =(", ").join([a.name for a in paper.authors])
            pub_paper =paper.published.strftime("%m/%d/%Y")
            d = f"The following is a summary of the paper: {paper.title}\n\nAuthors:{authors}\n\nDate:{pub_paper}\n\nSummary: {paper.summary}"
#            print(d)
            abstract_documents.append(Document(d))


        return arxiv_documents + abstract_documents

    def load_papers_and_abstracts(
            self,
            search_query: str,
            papers_dir: Optional[str] = ".papers",
            max_results: Optional[int] = 10,
    ) -> Tuple[List[Document], List[Document]]:
        """Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

        Args:
            search_query (str): A topic to search for (e.g. "Artificial Intelligence").
            papers_dir (Optional[str]): Locally directory to store the papers
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects representing the papers themselves
            List[Document]: A list of Document objects representing abstracts only
        """
        import arxiv

        arxiv_search = arxiv.Search(
            query=search_query,
            id_list=[],
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        search_results = list(arxiv_search.results())
        logging.debug(f"> Successfully fetched {len(search_results)} papers")

        if not os.path.exists(papers_dir):
            os.makedirs(papers_dir)

        paper_lookup = {}
        for paper in search_results:
            # Hash filename to avoid bad charaters in file path
            filename = f"{self._hacky_hash(paper.title)}.pdf"
            paper_lookup[os.path.join(papers_dir, filename)] = {
                "Title of this paper": paper.title,
                "Authors": (", ").join([a.name for a in paper.authors]),
                "Date published": paper.published.strftime("%m/%d/%Y"),
                "URL": paper.entry_id,
                # "summary": paper.summary
            }
            paper.download_pdf(dirpath=papers_dir, filename=filename)
            logging.debug(f"> Downloading {filename}...")

        def get_paper_metadata(filename):
            return paper_lookup[filename]

        SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
        arxiv_documents = SimpleDirectoryReader(
            papers_dir, file_metadata=get_paper_metadata
        ).load_data()
        # Include extra documents containing the abstracts
        abstract_documents = []
        for paper in search_results:
            d = f"The following is a summary of the paper: {paper.title}\n\nSummary: {paper.summary}"
            abstract_documents.append(Document(d))

        # Delete downloaded papers
        try:
            for f in os.listdir(papers_dir):
                os.remove(os.path.join(papers_dir, f))
                logging.debug(f"> Deleted file: {f}")
            os.rmdir(papers_dir)
            logging.debug(f"> Deleted directory: {papers_dir}")
        except OSError:
            print("Unable to delete files or directory")

        return arxiv_documents, abstract_documents


#test = ArxivReader_mod_search()
#test.load_data(search_query='quantum gravity',
#					  max_results=3, search_criterion =1)