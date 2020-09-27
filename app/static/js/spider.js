<script src="jquery.json-2.2.js"></script>

// var inputFileName = {'key': 'value', 'jian': 'zhi'};
// inputFileName = JSON.stringify(inputFileName);
// var obj = JSON.parse(JSON.stringify(inputFileName));
var obj = {'key': 'value', 'jian': 'zhi','sss':{'da':5,'dasd':5522}}
var ob = $.toJSON(obj);
console.log(ob)

function isEmptyObject(obj) {
  for (var key in obj) {
    return false;
  }
  return true;
}
var s = isEmptyObject(obj)
console.log(s)
for (var key in obj) {
　　var item = obj[key];
console.log(typeof item);

　　console.log(key,item); //AA,BB,CC,DD

}
console.log(obj.key);
console.log(obj);