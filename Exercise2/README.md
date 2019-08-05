其實切分index方式有很多  
我在這段script中有兩種，其中一些注解掉了，目前用的是世晟的方法  
也就是這段  
#index number in test  
其實我下面這樣的也是可以，如果採用請再進行修改，test_indexs = random.sample(range(133885), int(133885/10))，這邊已經對檔案給下標了
剩下的只是append一個值回去而已  
#append number into test set  

另外在ECFP方面必須要注意，轉之前給他是list，例如說 [SMILES1, SMILES2, SMILES3,...]  
轉完之後會是[[ECFP1], [ECFP2],...]，list裡面也是list  
這樣丟np轉array才不會有問題，如果將SMILES跟 Heat formation分開存再單純把SMILES轉ECFP配對會有問題(因為我試過，當然你可以解決也是可以用就不用每次都暫存在ram)  


注意：  
build model的時候一定要有輸入跟輸出，不要跟我一樣只有一層輸入一直出錯找不到原因  
值得注意的是輸出不填activation funcion = activation function(None) = activation function(linear)  
另外在這個地方  
loss, acc = model.evaluate(x_test, y_test, batch_size=256)  
會出錯也就是float64錯誤  
根據莫凡theano教學，定義dmattrix = float64, fmattrix = float32, 如果我記錯就算了，反正就是大概意思  
所以從中得到啟發要定義mattrix才不會出錯所以  
model.compile(loss='mean_squared_error', optimizer=sgd, metrics = ['accuracy'])   
後面的metrics為必須  

