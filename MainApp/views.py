from django.shortcuts import render
import pandas as pd
# Create your views here.
def index(request):
    # reading the text file
    data = pd.read_csv('NIFTY_F1_Xm8mAtb.txt')

    # creating data as data frame
    data = pd.DataFrame(data)

    # parse the time.
    data['TIME'] = pd.to_datetime(data['TIME'])
    # make the time the index.
    data = data.set_index("TIME")

    # group in 5-minute chunks.
    timeframe = data.resample('1H').agg({'OPEN': 'first',
                           'HIGH': 'max',
                           'LOW': 'min',
                           'CLOSE': 'last'})
    timeframe_html = timeframe.to_html()
    print(timeframe_html) # for testing purpose

    # minimum value of ohcl
    open = timeframe['OPEN'].min()
    high = timeframe['HIGH'].max()
    close = timeframe['CLOSE'].mean()
    low = timeframe['LOW'].min()

    print(open,high,close,low)

    context = {'data':timeframe_html,'open':open, 'high':high, 'close':close, 'low':low}
    template = 'index.html'
    return render(request, template, context)