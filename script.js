let arr = new Array(100).fill(0).map((x,i)=>{
     if (i%2 ==0) return "even"
     else return "odd"
})


arr.forEach((x,i)=>{
        console.log(i+"="+x)

    })


