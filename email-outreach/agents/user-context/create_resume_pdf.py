import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(file_path, text):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    text_object = c.beginText(40, height - 40)
    text_object.setFont("Helvetica", 10)
    
    for line in text.split('\\n'):
        text_object.textLine(line)
        
    c.drawText(text_object)
    c.save()

resume_text = """
**John Doe**
Software Engineer
john.doe@email.com | (123) 456-7890 | linkedin.com/in/johndoe

**Summary**
Innovative Software Engineer with 5+ years of experience in developing scalable web applications. Proficient in Python, JavaScript, and cloud technologies.

**Experience**
*   **Senior Software Engineer**, Tech Solutions Inc. (2020 - Present)
    *   Led a team of 5 engineers in developing a new user analytics platform.
    *   Improved application performance by 30%.
*   **Software Engineer**, Web Innovators (2018 - 2020)
    *   Developed and maintained client-side features using React.

**Education**
*   **B.S. in Computer Science**, University of Technology (2014 - 2018)

**Skills**
*   **Programming**: Python, JavaScript, Java
*   **Frameworks**: React, Django, Flask
*   **Cloud**: AWS, Docker
"""

if __name__ == "__main__":
    # Get the absolute path for the output file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    output_path = os.path.join(dir_path, "sample-resume.pdf")
    
    create_pdf(output_path, resume_text)
    print(f"{output_path} created successfully.")
