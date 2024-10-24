default_prompt = """
        Generate a 7-8 sentence summary about the country using the following data: {country_details}. 
        Please include important aspects like the country's economy, population, surface area, and tourism. 
        Whenever you will get very large values, round them into millions or billions. 
        For ex- $1,380,004 should be displayed as $1.38 million.
        Provide a informative summary.
"""

pop_density_prompt = """
        Create a 7-8 sentence summary about the country's population density and other parameters, 
        based on the following data: {country_details}. 
        Discuss how the population compares to the country's surface area to describe whether the country is 
        densely or sparsely populated. 
        Whenever you will get very large values, round them into millions. 
        For ex- $1,380,004 should be displayed as $1.38 million.
        Provide a informative summary.
    """

trade_prompt = """
        Generate a 7-8 sentence summary focusing on the country, using the following data: {country_details}. 
        Highlight the country's GDP,imports, export, GDP growth and currency comparison . 
        Convert large numeric values like GDP or trade figures into millions or billions
        For ex- $1,380,004 should be $1.38 million.
        Describe the country’s economic standing.
    """

import_export_prompt = """
        Summarize the country's imports and exports in 7-8 sentences using the following data: {country_details}. 
        Discuss the country’s GDP, import and export. 
        Convert large numeric values like GDP or trade figures into millions or billions
        For ex- $1,380,004 should be $1.38 million.
        The summary should give a clear picture of the country's global trade position.

    """

