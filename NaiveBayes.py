import sys
import re
import math
import csv

inputTable = [[[] for x in range(0)] for y in range(4601)] 
dividedInputTable = [[] for i in range(5)]		#should instead make it a 2d table
columnAvg = [0.10455,0.21301,0.28066,0.065425,0.31222,0.095901,0.11421,0.10529,0.090067,0.23941,0.059824,0.5417,0.09393,0.058626,0.049205,0.24885,0.14259,0.18474,1.6621,0.085577,0.80976,0.1212,0.10165,0.094269,0.5495,0.26538,0.7673,0.12484,0.098915,0.10285,0.064753,0.047048,0.097229,0.047835,0.10541,0.097477,0.13695,0.013201,0.078629,0.064834,0.043667,0.13234,0.046099,0.079196,0.30122,0.17982,0.0054445,0.031869,0.038575,0.13903,0.016976,0.26907,0.075811,0.044238,5.1915,52.173,283.29]		
Pspam = 0.394
PNspam = 0.606
def scannInfo(file):
	isRightHandS = False
	f = open (file, 'r')
	
	with open(file) as infile:
		rowcount = 0
		for line in infile:
			line = line.rstrip()
			line_split = line.split(',')	#use the space to split the inputs
			elementNum = len(line_split)
			for idx, val in enumerate( line_split ):
			
				inputTable[rowcount].append( val )
		
			rowcount = rowcount + 1
			
def divideFold():			#need to divide the folds into 5 groups, and do the mode of 5
	for idx, val in enumerate( inputTable ):
	
		if idx % 5 == 0:
			dividedInputTable[ 0 ].append( val )
		elif idx % 5 == 1:
			dividedInputTable[ 1 ].append( val )				
		elif idx % 5 == 2:
			dividedInputTable[ 2 ].append( val )		
		elif idx % 5 == 3:
			dividedInputTable[ 3 ].append( val )		
		elif idx % 5 == 4:
			dividedInputTable[ 4 ].append( val )

def k_fold(dividedInputTable):			# need to check the false positive and the false negative #concern something to get wrong, the k fold is for calculating the confusion matrix, average them
	print("Iteration\t","numerofPositiveSamplesInTraining\t","numberOfNegativeSamplesInTraininig\t","NumberofPositiveSamplesInDevelopment\t","NumberOfNegativeSamplesInDevelopment")
	averageList = [0 for i in range(10)]
	temp = 0
	DataStorage=[]
	errorArray =[]
	for idx, val in enumerate( dividedInputTable ):
		tempError=[]
		testData = dividedInputTable[idx]# getting the train data
		trainData = 0
		for idx1, val1 in enumerate( dividedInputTable ):	#makinng the train case
			if idx1 != idx:	#combine the table 
				if trainData == 0:
					trainData = dividedInputTable[idx1]
				else:
					trainData = trainData + dividedInputTable[idx1]	
		tempString =str(idx+1)
		temp = calculateTrainModelBasedOnMajor(trainData, testData)
		
	
		DataStorage.append(temp)	#FP,FN, overallError,posicount, negacount	for test
		

		
		print("traindatasize is ", len(trainData))
		print(idx+1,"\t\tFP",temp[0],"prob ",temp[0]/temp[3])#fn/neg  fp/posi 
		print(idx+1,"\t\tFN",temp[1],"prob",temp[1]/temp[4])
		print(idx+1,"\t\t",temp[2])
		print(idx+1,"\t\terrornum",temp[3])
		print(idx+1,"\t\ttrue",temp[4])

		
	
		for idx1, val1 in enumerate( temp ):
			averageList[idx1] = averageList[idx1] + temp[idx1]
	

		
	for idx1, val1 in enumerate( averageList ):
		averageList[idx1] = averageList[idx1]/5


def calculateTrainModelBasedOnMajor(trainData, testData):#think about this part of the code again, and finish it tomorrow
	errorArray = []	
	for idx, val in enumerate( trainData ):		
		if float(val[56]) > columnAvg[ 56 ]:	#to check if the last column is 0 or 1 to determine to probability, in this case, it is abvavg,spam
			errorArray.append(1)	
		else:
			errorArray.append(0)	
	errorNum = 0
	trueNum = 0
	FP = 0 	#0,1
	FN = 0	#1,0
	realValue = getRealValue(testData)
	for idx, val in enumerate( realValue ):
		if int(val) != errorArray[idx]:
			if int(val) == 1:
				FP = FP+1
			errorNum = errorNum + 1
		else:
			if int(val) == 0:
				FN = FN +1
			trueNum = trueNum + 1
			
	resultArray =[]
	FN = checkZeroCase(FN) #fn/neg  fp/posi 
	FP = checkZeroCase(FP)
	overallError = (FN+FP)/(errorNum+trueNum)
	resultArray.append(FP)
	resultArray.extend( [FN,overallError, errorNum,trueNum])
	
	return	resultArray				
	
def calculateTrainModel(trainData, testData):		#to do one fold
	
	PabvAvgSpCount = [0 for i in range(57)]
	PblAvgSpCount = [0 for i in range(57)]
	PabvAvgNSpCount = [0 for i in range(57)]
	PblAvgNSpCount = [0 for i in range(57)]
	
	for idx, val in enumerate( trainData ):	
		for idx1, val1 in enumerate( val ):
			if idx1 < 57:					#don't want to compare the last column
				if int(val[57]) == 1:
					if float(val1) > columnAvg[ idx1 ]:	#to check if the last column is 0 or 1 to determine to probability, in this case, it is abvavg,spam
						PabvAvgSpCount[idx1] =  1 + PabvAvgSpCount[idx1]
					else:
						PblAvgSpCount[idx1] =  1 + PblAvgSpCount[idx1] 
					
				else:
					if float(val1) > columnAvg[ idx1 ]:	#to check if the last column is 0 or 1 to determine to probability, in this case, it is abvavg,spam
						PabvAvgNSpCount[idx1] =  1 +PabvAvgNSpCount[idx1]
						
					else:
						PblAvgNSpCount[idx1] =  1 + PblAvgNSpCount[idx1]
	
	tempSumSPCount = 0
	tempSumNSPCount = 0		#the error should be appear here in the model
		
	for idx1, val1 in enumerate( PblAvgSpCount ):
		tempSumSPCount = PabvAvgSpCount[idx1] + PblAvgSpCount[idx1]
		tempSumNSPCount = PabvAvgNSpCount[idx1] + PblAvgNSpCount[idx1]
		
		PabvAvgSpCount[idx1] = float("{0:.3f}".format(PabvAvgSpCount[idx1]/tempSumSPCount))	#countSp
		PblAvgSpCount[idx1] = float("{0:.3f}".format(PblAvgSpCount[idx1]/tempSumSPCount)) 	#countSp
		PabvAvgNSpCount[idx1 ] = float("{0:.3f}".format(PabvAvgNSpCount[idx1]/ tempSumNSPCount)) 	#countNSp
		PblAvgNSpCount [idx1 ] = float("{0:.3f}".format(PblAvgNSpCount [idx1]/ tempSumNSPCount)) 	#countNSp

		
	#test data error
	outputValueTest = alternativeCalculation(PabvAvgSpCount,PabvAvgNSpCount, PblAvgSpCount, PblAvgNSpCount, testData ) #the test ratio
	#train data error
	outputValueTrain = alternativeCalculation(PabvAvgSpCount,PabvAvgNSpCount, PblAvgSpCount, PblAvgNSpCount, trainData ) #the train ratio
	outputValue = outputValueTest + outputValueTrain
	

	return outputValue#probArray#outputValue

def alternativeCalculation(PabvAvgSpCount,PabvAvgNSpCount, PblAvgSpCount, PblAvgNSpCount, testData ):
	errorArray =[]
	realValue = getRealValue(testData)
	negCount = 0
	posiCount = 0
	FNCount = 0
	FPCount = 0
	output = 0
	for idx, val in enumerate( testData ):	#add the data to every rows 
		ProbPoTotal = Pspam				#from the left multiply until the right side
		ProbNeTotal = PNspam
		for idx1, val1 in enumerate( val ):
			
			if idx1 < 57:  #one of the patterns here is that posi is always less than nega, but why?
				if float(val1) > columnAvg[ idx1 ]:
					ProbPoTotal = ProbPoTotal * checkZeroCase( PabvAvgSpCount[ idx1 ] ) 
					ProbNeTotal = ProbNeTotal * checkZeroCase( PabvAvgNSpCount[ idx1 ] ) 
				else:
					
					ProbPoTotal = ProbPoTotal * checkZeroCase( PblAvgSpCount [ idx1 ] ) 
					ProbNeTotal = ProbNeTotal * checkZeroCase( PblAvgNSpCount [ idx1 ] )  
		if 	ProbPoTotal > ProbNeTotal:
			output = 1
		else:	
			output = 0
			
		if int( realValue[idx] ) == 1: 
			if  output == 0:		
				FNCount = FNCount +1
			negCount = negCount + 1
		else:
			if output == 1:
				FPCount = FPCount +1		
			posiCount = posiCount + 1			
	FP = FPCount/	posiCount  #posiCount	#68/363
	FN = FNCount / negCount		#31/558
	overallError = (FPCount+FNCount)/(negCount+ posiCount)
	errorArray.append(FP)
	errorArray.extend([ FN, overallError, posiCount, negCount])
	return 	errorArray

	
def getRealValue(testData):
	realValue = []
	for idx, val in enumerate( testData ):	
		realValue.append(val[-1])
	return realValue
			
	
def checkZeroCase(value):
	if value == 0:
		return  0.0014
	else: 
		return value
		
file = sys.argv[1]
test = scannInfo(file)
divideFold()			
k_fold(dividedInputTable)

