//===========================
// Counter Animation
//===========================

const counters=document.querySelectorAll(".counter");

const speed=120;

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

const counter=entry.target;

const target=+counter.dataset.target;

const update=()=>{

const value=+counter.innerText;

const increment=target/speed;

if(value<target){

counter.innerText=Math.ceil(value+increment);

requestAnimationFrame(update);

}

else{

counter.innerText=target;

}

};

update();

observer.unobserve(counter);

}

});

});

counters.forEach(counter=>observer.observe(counter));