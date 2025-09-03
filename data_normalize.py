import re
import emoji
import pandas as pd

input_file = "Enter the file location here"
output_file = "Enter location of output file here"
slang_df = pd.read_csv("hf://datasets/theonlydo/indonesia-slang/slang-indo.csv")

def datacleansing(text):
    if pd.isna(text):  #Handle NaN values
        return ""
    text = str(text).lower()
    text = re.sub('[^0-9a-zA-Z]+',' ',text)
    text = re.sub('\n',' ',text) #Removing new lines in data
    text = re.sub('rt',' ',text) #Removing retweet words
    text = re.sub('user',' ',text) #Removing user words
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text) #Removing URLs
    text = re.sub(' +',' ',text) #Removing extra spaces
    text = re.sub(r'[^\x00-\x7f]',r' ',text) #Removing non-ascii
    text = emoji.replace_emoji(text, replace='') #Removing emojis
    return text.strip()

def replace_slang(text, slang_dict):
    words = text.split()
    replaced_words = [slang_dict.get(word, word) for word in words]
    return ' '.join(replaced_words)

#Create slang dictionary from the loaded dataframe
slang_dict = dict(zip(slang_df['slang'], slang_df['formal']))

#Read CSV file
print("Reading CSV File...")
df = pd.read_csv(input_file)
print(f"Total data: {len(df)} rows")

#Show available columns and ask user to select
print(f"\nAvailable columns: {list(df.columns)}")
text_column = input("Enter the name of the column containing the text to be cleaned up: ").strip()

#Validate selected column
while text_column not in df.columns:
    print(f"Column '{text_column}' not found!")
    print(f"Available columns: {list(df.columns)}")
    text_column = input("Enter the correct column name: ").strip()

print(f"Using column: {text_column}")

#Ask user about export preference
print("\nExport options:")
print("1. Only cleaned text (1 column)")
print("2. All original columns with text column replaced by cleaned text")
export_choice = input("Choose export option (1 or 2): ").strip()

while export_choice not in ['1', '2']:
    print("Please enter 1 or 2")
    export_choice = input("Choose export option (1 or 2): ").strip()

export_only_cleaned = (export_choice == '1')
print(f"Export mode: {'Only cleaned text' if export_only_cleaned else 'All columns with cleaned text'}")

#Process each row with progress
print("Processing data...")
cleaned_texts = []
for i, text in enumerate(df[text_column]):
    cleaned = datacleansing(text)
    #Apply slang replacement after cleaning
    cleaned = replace_slang(cleaned, slang_dict)
    cleaned_texts.append(cleaned)
    if (i + 1) % 100 == 0:  #Progress setiap 100 data
        print(f"Processed: {i + 1}/{len(df)}")

#Create DataFrame based on user choice
if export_only_cleaned:
    #Option 1: Only cleaned text
    result_df = pd.DataFrame({'cleaned_text': cleaned_texts})
else:
    #Option 2: All original columns with text column replaced by cleaned text
    result_df = df.copy()
    result_df[text_column] = cleaned_texts  #Replace original column with cleaned text

#Save to a new CSV file
result_df.to_csv(output_file, index=False)
print(f"Results saved to: {output_file}")
print(f"Columns in output file: {list(result_df.columns)}")

#Show sample results
print("\nSample results:")
if export_only_cleaned:
    for i in range(min(3, len(cleaned_texts))):
        print(f"Cleaned:  {cleaned_texts[i]}")
        print("-" * 50)
else:
    for i in range(min(3, len(result_df))):
        print(f"Original: {df[text_column].iloc[i]}")
        print(f"Replaced: {result_df[text_column].iloc[i]}")
        print("-" * 50)


