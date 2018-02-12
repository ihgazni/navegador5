import re

#time-field      = 1*2DIGIT
def time_field(input):
    regex = re.compile("[0-9]{1,2}")
    if(regex.search(input) == None):
        return(0)
    else:
        return(1)

#hms-time        = time-field ":" time-field ":" time-field
def hms_time(input):
    regex_1 = re.compile("[0-9]:[0-9]:[0-9]")
    regex_2 = re.compile("[0-9]{2}:[0-9]{2}:[0-9]{2}")
    if(regex_1.search(input) == None):
        if(regex_2.search(input) == None):
            return(0)
        else:
            return(1)
    else:
        return(1)

#  time            = hms-time ( non-digit *OCTET )
def time(input):
    regex = re.compile("(([0-9]:[0-9]:[0-9])|([0-9]{2}:[0-9]{2}:[0-9]{2}))[\x00-\x2f\x3a-\xff][\x00-\xff]*")
    m = regex.search(input)
    if(m == None):
        return(0)
    else:
        return(1)

# year            = 2*4DIGIT ( non-digit *OCTET )
def year(input):
    regex = re.compile("[0-9]{2,4}[\x00-\x2f\x3a-\xff][\x00-\xff]*")
    m = regex.search(input)
    if(m == None):
        return(0)
    else:
        return(1)
#month   = ( "jan" / "feb" / "mar" / "apr" /"may" / "jun" / "jul" / "aug" /"sep" / "oct" / "nov" / "dec" ) *OCTET
def month(input):
    regex = re.compile("(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[\x00-\xff]*")
    m = regex.search(input)
    if(m == None):
        return(0)
    else:
        return(1)

#day-of-month    = 1*2DIGIT ( non-digit *OCTET )
def day_of_month(input):
    regex = re.compile("[0-9]{1,2}[\x00-\x2f\x3a-\xff][\x00-\xff]*")
    m = regex.search(input)
    if(m == None):
        return(0)
    else:
        return(1)

# non-digit       = %x00-2F / %x3A-FF
def non_digit(input):
    regex_str = "[\x00-\x2f\x3a-\xff]"
    regex = re.compile(regex_str)
    if(regex.search(input) == None):
        return(0)
    else:
        return(1)

# non-delimiter   = %x00-08 / %x0A-1F / DIGIT / ":" / ALPHA / %x7F-FF
def non_delimiter(input):
    regex_str = "[\x00-\x08\x0a-\x1f0-9:a-zA-Z\x7f-\xff]"
    regex = re.compile(regex_str)
    if(regex.search(input) == None):
        return(0)
    else:
        return(1)
#delimiter       = %x09 / %x20-2F / %x3B-40 / %x5B-60 / %x7B-7E
def delimiter(input):
    regex_str = "[\x09\x20-\x2f\x3b-\x40\x5b-\x60\x7b-\x7e]"
    regex = re.compile(regex_str)
    if(regex.search(input) == None):
        return(0)
    else:
        return(1)

#date-token      = 1*non-delimiter
def date_token(input):
    regex_str = "[\x00-\x08\x0a-\x1f0-9:a-zA-Z\x7f-\xff]+"
    regex = re.compile(regex_str)
    if(regex.search(input) == None):
        return(0)
    else:
        return(1)

#date-token-list = date-token *( 1*delimiter date-token )
def date_token_list(input):
    regex_str = "[\x00-\x08\x0a-\x1f0-9:a-zA-Z\x7f-\xff]+([\x09\x20-\x2f\x3b-\x40\x5b-\x60\x7b-\x7e]+ [\x00-\x08\x0a-\x1f0-9:a-zA-Z\x7f-\xff]+)*"
    regex = re.compile(regex_str)
    if(regex.search(input) == None):
        return(0)
    else:
        return(1)

#cookie-date     = *delimiter date-token-list *delimiter
def cookie_date(input):
    regex_str = "[\x09\x20-\x2f\x3b-\x40\x5b-\x60\x7b-\x7e]* [\x00-\x08\x0a-\x1f0-9:a-zA-Z\x7f-\xff]+([\x09\x20-\x2f\x3b-\x40\x5b-\x60\x7b-\x7e]+ [\x00-\x08\x0a-\x1f0-9:a-zA-Z\x7f-\xff]+)* [\x09\x20-\x2f\x3b-\x40\x5b-\x60\x7b-\x7e]*"
    regex = re.compile(regex_str)
    if(regex.search(input) == None):
        return(0)
    else:
        return(1)