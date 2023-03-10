
// CALENDAR FUNCTIONALITY
let calendar = document.querySelector('.calendar')
const month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

isLeapYear = (year) => {
    return (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) || (year % 100 === 0 && year % 400 ===0)
}

getFebDays = (year) => {
    return isLeapYear(year) ? 29 : 28
}

generateCalendar = async (month, year) => {
    let calendar_days = calendar.querySelector('.calendar-days')
    let calendar_header_year = calendar.querySelector('#year')
    let days_of_month = [31, getFebDays(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    calendar_days.innerHTML = ''

    let currDate = new Date()
    if (month > 11 || month < 0) month = currDate.getMonth()
    if (!year) year = currDate.getFullYear()

    let curr_month = `${month_names[month]}`
    month_picker.innerHTML = curr_month
    calendar_header_year.innerHTML = year

    // get first day of month
    let first_day = new Date(year, month, 1)
    let day_num = 0

    for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {
        let day = document.createElement('a')
        if (i >= first_day.getDay()) {
            // day.classList.add('calendar-day-hover')

            curr_month = month+1
            day_num = i - first_day.getDay() + 1
            day.href = `/daily_tracker/${year}-${curr_month}-${day_num}`
            day.innerHTML = day_num
            day.innerHTML += `<span></span>
                            <span></span>
                            <span></span>
                            <span></span>`
            if (i - first_day.getDay() + 1 === currDate.getDate() && year === currDate.getFullYear() && month === currDate.getMonth()) {
                day.classList.add('curr-date')
            }

            let {result:is_logged} = await get_daily_tracker_check(curr_month, day_num, year)
            if(is_logged == true) {
                day.classList.add('calendar-day-logged');
            }
        }
        calendar_days.appendChild(day)
    }
}

async function get_daily_tracker_check(month, day_num, year) {
    const response = await fetch(`http://localhost:5000/calendar_builder/${month}/${day_num}/${year}`);
    const is_already_logged = await response.json();
    return is_already_logged;
}

let month_list = calendar.querySelector('.month-list')

month_names.forEach((e, index) => {
    let month = document.createElement('div')
    month.innerHTML = `<div data-month="${index}">${e}</div>`
    month.querySelector('div').onclick = () => {
        month_list.classList.remove('show')
        curr_month.value = index
        generateCalendar(index, curr_year.value)
    }
    month_list.appendChild(month)
})

let month_picker = calendar.querySelector('#month-picker')

month_picker.onclick = () => {
    month_list.classList.add('show')
}

let currDate = new Date()
let curr_month = {value: currDate.getMonth()}
let curr_year = {value: currDate.getFullYear()}

generateCalendar(curr_month.value, curr_year.value)

document.querySelector('#prev-year').onclick = () => {
    --curr_year.value
    generateCalendar(curr_month.value, curr_year.value)
}

document.querySelector('#next-year').onclick = () => {
    ++curr_year.value
    generateCalendar(curr_month.value, curr_year.value)
}


// SCROLL TO TOP
const toTopButton = document.getElementById("scroll-to-top");

window.onscroll = () => {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        toTopButton.style.display = "flex";
    } else {
        toTopButton.style.display = "none";
    }
};

const scrollToTop = () => {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
};



// COLOR THEME
// let root_variables = document.querySelector(':root'); // get the root element

// function color_theme_toggle() {
//     // style (properties and values) for the root
//     let root = getComputedStyle(root_variables);
//     // value of the --blue variable
//     let tan_color_code = root.getPropertyValue('--tan');
//     console.log(tan_color_code);

//     if(tan_color_code == "#dac8b6") {  //light mode
//         // set the value of variable --blue to another value (in this case "lightblue")
//         root_variables.style.setProperty('--blue', 'lightblue');

//         // --maroon: #603143;
//         // --light-maroon: #927681;
//         // --dark: #202B27;
//         // --grey: #a6a9a2;
//         // --tan: #dac8b6;
//         // --tapue: #d5d5d3;
//         // --calendar-bg-main: #fdfdfd;
//         // --calendar-hover: #efeeee;
//         // --shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
//     }
//     else if(tan_color_code == "#000") {  // dark mode

//     }
// }