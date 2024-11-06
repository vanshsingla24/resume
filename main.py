import fitz  # PyMuPDF for PDF text extraction
import streamlit as st
import openai
from jinja2 import Template
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your OpenAI API key
openai.api_key = "sk-ZAuml8OCrSi1TPQAb2QJ5m4wrzc3VPAD4uNGsx1xcbT3BlbkFJsXDibEybBi3sCH3EEh1YZ7Ur6bWrGCUIqWOYZZuFoA"  # Replace with your actual API key

# HTML template with enhanced project display
#\\ Updated HTML template with all details in Professional Experience section
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Summary</title>
</head>
<body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.2;">
    <table style="width: 100%; border-collapse: collapse; margin: 0 auto; max-width: 800px; line-height: 1.3; page-break-inside: avoid;">
        <tbody>
        
        <!-- Header with Logo -->
        <tr colspan="3" style="border-bottom: 5px solid #3A5998;">
            <td style="text-align: left; padding: 10px; color: #454545; font-size: 1.5em; font-weight: bold;">{{ name }}</td>
            <td></td>
            <td style="text-align: right; padding: 10px;">
                <img src="/home/vansh.singla/Downloads/kellton/resume/image/logo.png" alt="Logo" style="height: 24px; width: auto;" />
            </td>
        </tr>
        
        <!-- Summary Section -->
        <tr>
            <td colspan="3" style="padding: 5px;">
                <h2 style="color: #3A5998; padding: 5px 0; margin: 5px 0;">Summary</h2>
                <p style="color: #666; padding: 5px; border-top: 2px solid #999999;"> <!-- Updated padding and border color -->
                    {{ summary or 'No Summary Available' }}
                </p>
            </td>
        </tr>
        
        <!-- Technical Skills Section -->
        <tr>
            <td colspan="3" style="padding: 5px;">
                <h2 style="color: #3A5998; margin: 5px 0; padding: 5px 0;">Technical Skills</h2>
                <table style="width: 100%; border-collapse: collapse; border-top: 2px solid #999999;"> <!-- Updated border color -->
                    {% for i in range(0, skills|length, 3) %}
                    <tr>
                        {% for skill in skills[i:i+3] %}
                        <td style="padding: 5px; text-align: left; width: 33.33%; color: #555;">
                            <img src="/home/vansh.singla/Downloads/kellton/resume/image/arrow.svg" alt="arrow icon" 
                                 style="width: 12px; height: 12px; vertical-align: middle; margin: -3px 5px 0px 0px;">
                            {{ skill }}
                        </td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
            </td>
        </tr>
        
        <!-- Professional Experience Section with Complete Details -->
        <tr>
            <td colspan="3" style="padding: 5px;">
                <h2 style="color: #3A5998; padding: 5px 0; margin: 5px 0;">Professional Experience</h2>
                <table style="width: 100%; border-collapse: collapse; border-top: 2px solid #999999;"> <!-- Updated border color -->
                    {% for job in experience %}
                    <tr>
                        <td style="padding:14px 0 5px 0; font-weight: bold; color: #3A5998;">{{ job.company }}</td>
                    </tr> 
                    <tr>
                        <td style="padding:5px; color: #555;">
                            <strong>Title:</strong> {{ job.title }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:5px; color: #555;">
                            <strong>Dates:</strong> {{ job.start_date }} - {{ job.end_date or 'Present' }}
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:5px; color: #666;">
                            <strong>Description:</strong> {{ job.description }}
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            </td>
        </tr>
        
        <!-- Education Section -->
        <tr>
            <td colspan="3" style="padding: 5px;">
                <h2 style="color: #3A5998; padding: 5px 0; margin: 5px 0;">Education</h2>
                <table style="width: 100%; border-collapse: collapse; border-top: 2px solid #999999;"> <!-- Updated border color -->
                    {% for edu in education %}
                    <tr>
                        <td style="padding:5px 0; color: #454545; font-weight: bold;">{{ edu.institution }}</td>
                    </tr> 
                    <tr>
                        <td style="padding:5px 0; color: #454545;">{{ edu.degree }}</td>
                    </tr> 
                    {% endfor %}
                </table>
            </td>
        </tr>
        
        <!-- Projects Section with Detailed Display -->
        {% if projects %}
        <tr>
            <td colspan="3" style="padding: 5px;">
                <h2 style="color: #3A5998; padding: 5px 0; margin: 5px 0;">Projects</h2>
                <table style="width: 100%; border-collapse: collapse; border-top: 2px solid #999999;"> <!-- Updated border color -->
                    {% for project in projects %}
                    <tr>
                        <td style="padding:5px; color: #454545; font-weight: bold;">{{ project.project_name }}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px; color: #666;"><strong>Description:</strong> {{ project.description }}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px; color: #666;"><strong>Technologies:</strong> {{ ', '.join(project.technologies) }}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px; color: #666;"><strong>Role:</strong> {{ project.role }}</td>
                    </tr>
                    <tr>
                        <td style="padding:5px; color: #666;"><strong>Duration:</strong> {{ project.duration }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </td>
        </tr>
        {% endif %}
        
        <!-- Achievements Section -->
        {% if achievements %}
        <tr>
            <td colspan="3" style="padding: 5px;">
                <h2 style="color: #3A5998; padding: 5px 0; margin: 5px 0;">Achievements</h2>
                <table style="width: 100%; border-collapse: collapse; border-top: 2px solid #999999;"> <!-- Updated border color -->
                    {% for achievement in achievements %}
                    <tr>
                        <td style="padding:5px; color: #454545;">{{ achievement }}</td>
                    </tr>
                    {% endfor %}
                </table>
            </td>
        </tr>
        {% endif %}
        
        <!-- Languages Section -->
        {% if languages %}
        <tr>
            <td colspan="3" style="padding: 5px;">
                <h2 style="color: #3A5998; padding: 5px 0; margin: 5px 0;">Languages</h2>
                <table style="width: 100%; border-collapse: collapse; border-top: 2px solid #999999;"> <!-- Updated border color -->
                    <tr>
                        <td style="padding:5px; color: #454545;">{{ ', '.join(languages) }}</td>
                    </tr>
                </table>
            </td>
        </tr>
        {% endif %}
        </tbody>
    </table>
</body>
</html>

"""


def preprocess_parsed_data(parsed_data):
    parsed_data['name'] = parsed_data.get('name', 'No Name Provided')
    parsed_data['email'] = parsed_data.get('email', 'No Email Provided')
    parsed_data['phone'] = parsed_data.get('phone', 'No Phone Provided')
    parsed_data['location'] = parsed_data.get('location', 'No Location Provided')
    parsed_data['summary'] = parsed_data.get('summary', 'No Summary Available')
    parsed_data['skills'] = parsed_data.get('skills', [])
    parsed_data['experience'] = parsed_data.get('experience', [])
    parsed_data['education'] = parsed_data.get('education', [])
    parsed_data['certifications'] = parsed_data.get('certifications', [])
    parsed_data['projects'] = parsed_data.get('projects', [])
    parsed_data['achievements'] = parsed_data.get('achievements', [])
    parsed_data['languages'] = parsed_data.get('languages', [])
    return parsed_data

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Enhanced parse_resume_with_openai for detailed project extraction and lower temperature
def parse_resume_with_openai(resume_text):
    prompt = (
        "Extract the following information from this resume text in valid JSON format with keys: "
        "'name', 'email', 'phone', 'location', 'summary', 'skills' (as a list of individual skills), "
        "'experience' (as a list of dictionaries with keys 'company', 'title', 'description', 'start_date', 'end_date'), "
        "'education' (as a list of dictionaries with 'institution', 'degree', 'start_date', 'end_date'), "
        "'certifications', 'projects' (as a list of dictionaries with keys 'project_name', 'description', 'technologies' (list), 'role', 'duration'), "
        "'achievements', and 'languages'. "
        "Only return JSON with no extra explanations or formatting."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,  # Setting temperature to make responses more deterministic
        messages=[
            {"role": "system", "content": "You are a resume data extraction assistant."},
            {"role": "user", "content": f"{prompt}\n\n{resume_text}"}
        ]
    )
    
    generated_text = response['choices'][0]['message']['content'].strip()
    
    try:
        parsed_data = json.loads(generated_text)
        return parsed_data
    except json.JSONDecodeError:
        st.error("The model response is not valid JSON.")
        logging.error("Model response could not be parsed as JSON.")
        print("Generated text for inspection:", generated_text)
        return None

def generate_html(parsed_data, template_str):
    parsed_data = preprocess_parsed_data(parsed_data)
    template = Template(template_str)
    return template.render(parsed_data)

# Streamlit app
st.title("Resume Extractor and HTML Renderer")

uploaded_file = st.file_uploader("Upload a resume (PDF format)", type="pdf")

if uploaded_file is not None:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    resume_text = extract_text_from_pdf("temp_resume.pdf")

    parsed_data = parse_resume_with_openai(resume_text)

    if parsed_data and isinstance(parsed_data, dict):
        html_content = generate_html(parsed_data, html_template)
        st.markdown("### Extracted Resume in HTML Format")
        st.components.v1.html(html_content, height=1000, scrolling=True)

        st.download_button(
            label="Download Resume as HTML",
            data=html_content,
            file_name="resume.html",
            mime="text/html"
        )
    else:
        st.error("Failed to parse resume.")
