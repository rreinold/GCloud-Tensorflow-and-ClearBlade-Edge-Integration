/**
* @param {context} ctx - Object containing data and model information for this item.
*/
parser = (ctx) => {

  var dataFile = datasources.dataFile.latestData();
  var archFile = datasources.archFile.latestData();
  var trainFile = datasources.trainFile.latestData();

  // if(dataFile == null || archFile == null || trainFile == null) {
  //   alert("Please provide the necessary files for training");
  //   return;
  // }

  var encoded_data = btoa(dataFile);
  var encoded_arch = btoa(archFile);
  var encoded_train = btoa(trainFile);

  var url = "https://staging.clearblade.com/api/v/1/collection/a6c2e6d10bc2f183fca3c7d3d0fe01/TrainingFiles"

  var header = {
    "ClearBlade-UserToken" : datasources.authtoken.latestData(),
    "systemKey" : "92c4d0d30b9884faaac380f694b201",
    "collectionName" : "TrainingFiles"
  }

  var body = {
    "datafile" : encoded_data,
    "archfile" : encoded_arch,
    "trainfile" : encoded_train
  }

  fetch(url, {
        method:'POST',
        headers:header,
        body:JSON.stringify(body)
      }).then((resp) => resp.json())
      .then((data) => console.log(data));

  var data = ctx.widget.data;
  //console.log(data)
  
  if(datasources.datafilename.latestData() == undefined){
    data["dataFile"] = "processData.py"
  } else {
    data["dataFile"] = datasources.datafilename.latestData();
  }

  if(datasources.archfilename.latestData() == undefined){
    data["archFile"] = "model.py"
  } else{
    data["archFile"] = datasources.archfilename.latestData();
  }

  if(datasources.trainfilename.latestData() == undefined){
      data["taskFile"] = "task.py";
  } else {
      data["taskFile"] = datasources.trainfilename.latestData();
  }

  data["usertoken"] = datasources.authtoken.latestData();
  data["modelid"] = "9ed0fcd20b98a0f6e3af8ccd859d01"

  var clean = [];
  for (var i=0; i<datasources.cleanColumns.latestData().clean.length; i++){
    clean.push(datasources.cleanColumns.latestData().clean[i].item_id);
  }

  data["toClean"] = clean;
  datasources.send.sendData(JSON.stringify(data));
  alert("Data Sent for Training")

  // console.log(data)

  // return datasources.MY_CODE_SERVICE_NAME.sendData(ctx.widget.data).then((res) => {
  //     if (res.success) {
  //         console.log('Successfully created: ', res.results)
  //     } else {
  //         console.log('error: ', res.results)
  //     }
  //     return res
  // })

  return {}
}