<h1>MAAPA: Homework Helper</h1>
<h2>Table of Contents</h2>
<ol>
  <li>Motivation</li>
  <li>Description</li>
  <li>Stack Overview</li>
  <li>Project Evolution</li>
  <li>Download and Run</li>
</ol>
<h2>Motivation</h2>
I hated doing homework during online school. Scrolling through 500-page pdf textbooks to find answers deeply irritated me. Simply using Ctrl+F was not effective or accurate. I wanted to make a smarter and faster way to find answers from my textbooks.
<h2>Description</h2>
From the landing page, you can create an account or login to an existing account. You can find your stored pdfs under your account. When searching a pdf, MAAPA first returns a page where the answer to the question might be located, then a paragarph, and upon confirmation of the paragraph containing the answer from the user, MAAPA reads the paragraph to answer the question. If at any point, the user indicates that the page or paragraph returned do not contian the answer, MAAPA will return the next best page or paragraph. MAAPA uses a weighted tf-idf algorithm that weighs a medium frequency of words closer to a low frequency than a high frequency. This is because it was observed that textbooks tend to use the key-words present in questions often to explain them. MAAPA uses a pre-trained BERT model to read final paragraph to return an answer. MAAPA stores each user input from "correct page", "incorrect page", "correct paragraph", "incorrect paragraph", "correct answer", "incorrect answer" in a SQLite database for a potential retrain of BERT in the future.
<h2>Stack Overview</h2>
Python and Django for backend. Django, Bootstrap, HTML, CSS, and Javascript for frontend. SQLite and Django for database. Python and Javascript for AI implementation. Hosted on AWS Lightsail.
<h2>Project Evolution</h2>
Initially, the tf-idf algorithm and BERT neural network were coded in Python and running server-side. Unfortunately, the inexpensive AWS Lightsail server could not handle the computation and would frequently crash with multiple users. Slowly, each computationally intensive algorathm was re-coded using Javascript and set to run on the users browser. This reduced the probability of server crashes and provided a smoother user experience.
<h2>Download and Run</h2>
<ol>
  <li>Create an empty folder "MAAPA"</li>
  <li>Run "git clone https://github.com/KrishM123/MAAPA"</li>
  <li>Install Python 3.7 on your system</li>
  <li>Open and navigate to the MAAPA folder on command prompt</li>
  <li>Run "python -m venv venv\</li>
  <li>Activate the virtual evironment using "venv\Scripts\activate</li>
  <li>Run "pip install -r requirements.txt</li>
  <li>Run "python manage.py runserver"</li>
  <li>Copy and paste the local server address in chrome to run MAAPA</li>
</ol>
