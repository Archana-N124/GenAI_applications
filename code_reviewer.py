
import streamlit as st
import google.generativeai as  gemini

# Configure the api key

f = open("keys/.gemini.txt")
key = f.read()

gemini.configure(api_key=key)


def review_code(code):
    
    # Create a system prompt
    
    sys_prompt = f"Analyze the following Python code and identify and provide any errors or  potential bugs or areas of improvement :\n```python\n{code}\n```\nIf any issues are found, provide corrected code snippet."

    model = gemini.GenerativeModel(model_name="models/gemini-1.5-flash", 
                          system_instruction=sys_prompt)
    
    
    # Send the prompt to model
    
    response = model.generate_content(code)
    return response

    

def main():
    st.title("An AI Code Reviewer")

    # Getting user's code
    
    code = st.text_area("Enter your Python code:")
 

    if st.button("Generate"):
        if code:
            try:
                corrected_code = review_code(code)
                
                st.success("Bug report:")
                bug_report = corrected_code.text.split("Here's the corrected code:\n")[0]
                st.write(bug_report)

                st.success("Fixed code:")
                fixed_code = corrected_code.text.split("```python\n")[1].split("```")[0]
                st.code(fixed_code, language="python")
                
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter your code.")

        

if __name__ == "__main__":
    main()
   