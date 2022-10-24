def clean(df_main, df_slang, df_stop):
    
    import re
    from module.Cleansing_Text import Clean_text

    def Clean_slang(text):
        Slang_dict = dict(zip(df_slang['alay'], df_slang['normal'])) 
        holder = [] 
    
        for word in text.split(' '): 
        
            if word in Slang_dict.keys(): 
                word = Slang_dict[word] 
                holder.append(word) 
            else :
                holder.append(word) 
            
        return ' '.join(holder)

    def Clean_stop(text):
        holder = []
    
        for words in text.split(' '):
            if words in df_stop['kata'].values:
                holder.append(' ')
            else:
                holder.append(words)
    
        text = ' '.join(holder)
        text = re.sub(' +', ' ', text)
        text = text.strip() 
        return text

    
    def Clean_all(text):
        text = Clean_text(text)
        text = Clean_slang(text)
        text = Clean_stop(text)
        return text
    
    df_clean = df_main['Tweet'].apply(lambda x : Clean_all(x))

    return df_clean