


export default function formattedTime(iso_date_string) {
    const formatted_time = (direction) => {
        return formatted_time(info, direction)
    };
    return {
        formatted_time,
    }
}


function formatted_time(iso_date_string) {
    const date = new Date(iso_date_string);
    return date.toLocaleDateString()
}