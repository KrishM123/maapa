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
Python and Django for backend. Django, Bootstrap, HTML, CSS, and Javascript for frontend. SQLite and Django for database. Python and Javascript for AI implementation.
