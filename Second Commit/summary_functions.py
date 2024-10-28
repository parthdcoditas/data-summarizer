import prompts
from groq import Groq
import os
from app import client

def default_summary(country_data):
    country_details = f'''
        Country: {country_data[1]}
        GDP: {country_data[3]}
        Population: {country_data[2]}
        Exports: {country_data[6]}
        Surface Area: {country_data[5]}
        Tourists: {country_data[7]}
        '''
    try:     
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompts.default_prompt.format(country_details = country_details)}],
            model="llama3-8b-8192"  
        )

        summary = chat_completion.choices[0].message.content
        return summary

    except Exception as e:
        print(f"Error generating Groq summary: {e}")
        return f"Error generating summary: {e}"

def pop_density_summary(country_data):
    country_details = f'''
        Country: {country_data[1]}
        Population: {country_data[2]}
        Population Density: {country_data[9]}
        Population Growth: {country_data[10]}
        Sex Ratio: {country_data[12]}
        '''
    try:     
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompts.pop_density_prompt.format(country_details = country_details)}],
            model="llama3-8b-8192"  
        )

        summary = chat_completion.choices[0].message.content
        return summary

    except Exception as e:
        print(f"Error generating Groq summary: {e}")
        return f"Error generating summary: {e}"

def trade_summary(country_data):
    country_details = f'''
        Country: {country_data[1]}
        GDP: {country_data[3]}
        Imports: {country_data[5]}
        Exports: {country_data[6]}
        GDP Growth: {country_data[8]}
        Currency: {country_data[11]}
        '''
    try:     
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompts.trade_prompt.format(country_details = country_details)}],
            model="llama3-8b-8192"  
        )

        summary = chat_completion.choices[0].message.content
        return summary

    except Exception as e:
        print(f"Error generating Groq summary: {e}")
        return f"Error generating summary: {e}"

def import_export_summary(country_data):
    country_details = f'''
        Country: {country_data[1]}
        GDP: {country_data[3]}
        Imports: {country_data[5]}
        Exports: {country_data[6]}
        '''
    try:     
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompts.import_export_prompt.format(country_details = country_details)}],
            model="llama3-8b-8192"  
        )

        summary = chat_completion.choices[0].message.content
        return summary

    except Exception as e:
        print(f"Error generating Groq summary: {e}")
        return f"Error generating summary: {e}"
