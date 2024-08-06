# MAAPA: Homework Helper 📚

## Motivation 😤

I hated doing homework during online school. Scrolling through 500-page PDF textbooks to find answers deeply irritated me. Simply using Ctrl+F was not effective or accurate. I wanted to make a smarter and faster way to find answers from my textbooks.

## Description 📖

From the landing page, you can create an account or log in to an existing account. You can find your stored PDFs under your account. When searching a PDF, MAAPA first returns a page where the answer to the question might be located, then a paragraph, and upon confirmation of the paragraph containing the answer from the user, MAAPA reads the paragraph to answer the question. If at any point, the user indicates that the page or paragraph returned does not contain the answer, MAAPA will return the next best page or paragraph. MAAPA uses a weighted tf-idf algorithm that weighs a medium frequency of words closer to a low frequency than a high frequency. This is because it was observed that textbooks tend to use the keywords present in questions often to explain them. MAAPA uses a pre-trained BERT model to read the final paragraph to return an answer. MAAPA stores each user input from "correct page", "incorrect page", "correct paragraph", "incorrect paragraph", "correct answer", "incorrect answer" in a SQLite database for a potential retrain of BERT in the future.

## Stack Overview 🥞

- **Backend**: Python and Django
- **Frontend**: Django, Bootstrap, HTML, CSS, and Javascript
- **Database**: SQLite and Django
- **AI Implementation**: Python and Javascript
- **Hosting**: AWS Lightsail

## Project Evolution 🛠️

Initially, the tf-idf algorithm and BERT neural network were coded in Python and running server-side. Unfortunately, the inexpensive AWS Lightsail server could not handle the computation and would frequently crash with multiple users. Slowly, each computationally intensive algorithm was re-coded using Javascript and set to run on the users' browser. This reduced the probability of server crashes and provided a smoother user experience.

## Download and Run 🚀

1. Create an empty folder `MAAPA`.
2. Run the command:
`git clone https://github.com/KrishM123/MAAPA`
3. Install Python 3.7 on your system.
4. Open and navigate to the MAAPA folder on command prompt.
5. Set up the virtual environment:
`python -m venv venv`
6. Activate the virtual environment:
`venv\Scripts\activate`
7. Install dependencies:
`pip install -r requirements.txt`
8. Start the server:
`python manage.py runserver`
9. Copy and paste the local server address in chrome to run MAAPA.
