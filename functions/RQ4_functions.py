import pandas
from collections import defaultdict
import scipy.special

#This function read the file zone lookup and return a dictonary with as entrys the names of the boroughs and as values a list with the IDs of the associated zones
def boroughsIdentifyer():
    #We load the lookup tables with the names of the zones and the rispective codes
    zones = pandas.read_csv('taxi _zone_lookup.csv',sep=',', encoding='ISO-8859-1')
    
    boroughs = defaultdict(list)
    
    #We create the dicontary    
    for number,name in list(zip(zones["LocationID"].values,zones["Borough"].values)): 
        boroughs[name].append(number)
        
    #We delete the IDs associated to unknow zones considering them an error
    boroughs.pop('Unknown')
    
    #We return it
    return dict(boroughs)

#We define a function that will return a bidimensional data frame contaning the number of payment methods used for each borough
def payment_category(boroughs):
    
    #We prepare the list of methods
    methods = ['Credit card','Cash', 'No charge', 'Dispute']

    #and the dictonary to be filled
    payments_method = {borough:{method: 0 for method in methods} for borough in boroughs.keys()}

    #We create a list with the month numbers we are interested in
    months = ['0'+str(i) for i in range(1,7)]
    for month in months:
        
        #We load the file
        taxi = pandas.read_csv('yellow_tripdata_2018-'+month+'.csv',sep=',', encoding='ISO-8859-1')
        taxi = taxi[list(map(lambda x: x[2:7] == '18-'+month, taxi["tpep_pickup_datetime"].values))]
        
        #And we check the values in the file
        for borough in boroughs.keys():
            for p in (taxi.loc[taxi['PULocationID'].isin(boroughs[borough])])['payment_type'].values.tolist():
                if p == 1:
                    payments_method[borough]['Credit card'] += 1
                elif p == 2:
                    payments_method[borough]['Cash'] += 1
                elif p == 3:
                    payments_method[borough]['No charge'] += 1
                elif p == 4:
                    payments_method[borough]['Dispute'] += 1
    #We return the dictionary transformed in a data frame
    return pandas.DataFrame(payments_method)

#We define a function that will return the p-value of the chi-squared analysis for a matrix O of observations
def chi_2(O):
    
    #We register the number of columns, rows and the sum of all the elements of O
    r = len(O)
    c = len(O[0])
    t = sum(sum(O[i][j]for i in range(r)) for j in range(c))
    
    #We build the matrix of expected values E
    E = [[sum(O[i][k]for k in range(c))*sum(O[k][j]for k in range(r))/t for i in range(r)] for j in range(c)]
    E = [[E[j][i] for j in range(c)] for i in range(r)]
    
    #We compute the chi-squared-value of the matrix
    chi = sum(sum(((E[i][j]-O[i][j])**2)/E[i][j] for i in range(r)) for j in range(c))
    #His degree of freedom
    df = (r-1)*(c-1)

    #And finially the p-value
    p = 1-scipy.special.gammainc(df/2,chi/2)

    return p
