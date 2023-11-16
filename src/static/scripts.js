const btncopy = document.getElementById("btn-copy-reply");
const copy_text = document.querySelector(".copy-text");
/* document.addEventListener("mouseover",(event) => {
    // highlight the mouseenter target
    
    if (event.target == copy_text)
    {
        btncopy.classList.add("hover-active");
        btncopy.classList.remove("hover-inactive");
        console.log("Fired In")
    }
    else
    {
        btncopy.classList.remove("hover-active");
        btncopy.classList.add("hover-inactive");
        console.log("Fired Out") 
    }

  },
  true,
); */
btncopy.addEventListener("click", function() {
    let clipboardText = document.getElementById("reply");
    const storage = document.createElement('textarea');
    storage.value = clipboardText.innerHTML;
    clipboardText.appendChild(storage);

    // Select the text field
    storage.select();
    storage.setSelectionRange(0, 99999);
    // Copy the text in the fake `textarea` and remove the `textarea`
    navigator.clipboard.writeText(storage.value);
    clipboardText.removeChild(storage);

});


//copy-text hover 
copy_text.addEventListener("mouseenter",(event) => {
    // highlight the mouseenter target
    if (!btncopy.classList.contains("hover-active"))
    {
        btncopy.classList.add("hover-active");
        btncopy.classList.remove("hover-inactive");
       
    }
  },
  true,
);

 copy_text.addEventListener("mouseout",(event) => {
    if (btncopy.classList.contains("hover-active"))
    {
        btncopy.classList.remove("hover-active");
        btncopy.classList.add("hover-inactive");
        
    }
  },
  true,
); 