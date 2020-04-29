// Write a function deepEquals that takes two values and returns true only if they are the same value or are objects with 
// the same properties, where the values of the properties are equal when compared with a recursive call to deepEquals.
// To find out whether values should be compared directly (use the === operator for that) or have their properties compared, 
// you can use the typeof operator. If it produces an "object" for both values, you should do a deep comparison. 
// But you have to take one silly exception into account: because of a historical accident, typeof null also produces "object".
// The Object.keys function will be useful when you need to go over the properties of objects to compare them.


function deepEquals(a, b) {
    if (a == b) {
      return true;
    } 
    else if (typeof a == 'object'&& typeof b == 'object') {
        let keys = Object.keys(a).concat(Object.keys(b));
        for (p of keys) {
            if (typeof a[p] == 'object' && typeof b[p] == 'object') {
                if (deepEquals(a[p], b[p]) == false) {
                    return false;
                }
            } 
            else if (a[p] !== b[p]) {
                return false;
            }
        }
        return true;
    } 
    else {
        return false; 
    }
  }

obj1 = {
    fn:"Venu",
    ls:"Gopal"
}
obj2 = {
    fn:"Ravali",
    number:2019501013
}

obj3 = {
    fn:"Venu",
    ls:"Gopal"
}

str1 = "Venu"
str2 = 1947
str3 = "Gopal"

console.log(deepEquals(obj1,obj2))
console.log(deepEquals(obj1,obj3))
console.log(deepEquals(str2,str1))
console.log(deepEquals(str3,str1))
console.log(deepEquals(str1,str1))