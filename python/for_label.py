#path_infile = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\filtered\\tweets_2019-09-01.json'
PATH = 'C:\\Users\\niti.mishra\\Documents\\Personal\\cyberbullying\\data\\filtered\\'
output_dir = 'send_for_label'

def sendforlabel_tweets(path_infile, output_dir):

    # PATH
    PATH_data = Path(path_infile)
    
    # load and select reqd columns
    data = pd.read_json(PATH_data, lines=True)
    data_forlabel = data[['id', 'full_tweet']]
    
    #data_forlabel['no_hashtags'] = 
    #print(data_forlabel.head())

    # output
    path_outfile = Path.joinpath(PATH_data.parents[1], output_dir,  (PATH_data.stem + '.csv') )
    data_forlabel.to_csv(path_outfile, index=False, encoding = 'utf-8-sig')

for file in os.listdir(PATH + infile):
    print(file)
    sendforlabel_tweets(PATH=PATH, infile=infile, outfile=outfile, filename=file)

