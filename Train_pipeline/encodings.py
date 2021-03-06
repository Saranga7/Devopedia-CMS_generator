from libraries import *
from data_object import *
from functions import *
import warnings
warnings.filterwarnings('ignore')


def encoding_creation(temp_df,name):
    z_df=get_encoded_df(temp_df,name)
    folder_path='Train_preprocess'
    z_df.to_csv(os.path.join(folder_path,f'{name}.csv'),index=False)
    print(f'{name} encodings completed!\n')
    return z_df


if __name__=="__main__":

    print("Running encodings.py...\n\n")
    start_t=time.perf_counter()

    cmdline_params = {rows[0]:rows[1] for rows in reader(open(sys.argv[1], 'r'))}

    df=pd.read_csv(cmdline_params['raw_dataset'])

    print(df.shape)
    df=df[df.text.notnull()]
    
    df.reset_index(inplace=True,drop=True)
    print(df.shape)
    

    temp_df = df.copy(deep=True)              #to prevent creation of duplicate encoded axes later

    names=['Author','Title','YoP']

    create_encodings=functools.partial(encoding_creation,temp_df=temp_df)

    with concurrent.futures.ProcessPoolExecutor() as executor:              #Processing author, title, yop dataframes simulatenously
        result_dfs=[executor.submit(encoding_creation,temp_df,name) for name in names]

    print(result_dfs)

    # print('processing Author Encodings ...')
    # author_df=get_encoded_df(temp_df,'Author')
    # author_df.to_csv('author.csv',index=False)

    # print('processing Title Encodings ...')
    # title_df=get_encoded_df(temp_df,'Title')
    # title_df.to_csv('title.csv',index=False)

    # print('processing YoP Encodings ...')
    # yop_df=get_encoded_df(temp_df,'YoP')
    # yop_df.to_csv('yop.csv',index=False)

    folder_path='Train_preprocess'

    author_df=pd.read_csv(os.path.join(folder_path,"Author.csv"))
    title_df=pd.read_csv(os.path.join(folder_path,"Title.csv"))
    yop_df=pd.read_csv(os.path.join(folder_path,"YoP.csv"))

 
  
    author_encoded=pd.merge(author_df,df, on=['index', 'fname'],how='left')
    author_encoded.to_csv(os.path.join(folder_path,'Author_encoded.csv'),index=False)


    title_encoded=pd.merge(title_df,df,on=['index', 'fname'],how='left')
    title_encoded.to_csv(os.path.join(folder_path,'Title_encoded.csv'),index=False)
 
    yop_encoded=pd.merge(yop_df,df, on=['index', 'fname'],how='left')
    yop_encoded.to_csv(os.path.join(folder_path,'YoP_encoded.csv'),index=False)

    end_t=time.perf_counter()

    print(f"Encodings done in {(end_t-start_t)/60} minutes")







