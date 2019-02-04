function email_check()
{
	var ov=f.uemail.value;
	if(ov.length<=35)
    {
        var atpos=ov.indexOf("@");
	    var dotpos=ov.lastIndexOf(".");
	    if(atpos<1 || dotpos<atpos+2 || dotpos+2>=ov.length)
	    {
	    	document.getElementById("c").innerHTML="&#x2716";
	    	return false;
	    }
	    else
	    {
	    	document.getElementById("c").innerHTML="&#10004";
	    	return true;
	    }
    }
    else
    {
        document.getElementById("c").innerHTML="&#x2716";
        return false;
    }

}


function pwd_check()
{
    var p=f.upwd.value;
	if(p.length>=8 && p.length<=15)
	{
		document.getElementById("d").innerHTML="&#10004";
		return true;
	}
	else
	{

			document.getElementById("d").innerHTML="&#x2716";
			return false;
	}

}


function main()
{
	var v1=email_check();
	if(v1===true)
    {
        var v2=pwd_check();
        if(v2==true)
        {
            return true;
        }
        else
        {
            return false;
        }

    }
    else
    {
        return false;
    }
}


