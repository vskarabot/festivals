export default function chatTimes () {

    const now = new Date()
    const formatTimeDifference = (timestamp) => {
        const messageDate = new Date(timestamp) 
        const differenceMs = now - messageDate 
        
        const differenceSec = Math.floor(differenceMs / 1000) 
        const differenceMin = Math.floor(differenceSec / 60) 
        const differenceHour = Math.floor(differenceMin / 60) 
        const differenceDay = Math.floor(differenceHour / 24) 
        const differenceMonth = Math.floor(differenceDay / 30)
        const differenceYear = Math.floor(differenceMonth / 365)
    
        if (differenceYear > 0) {
            return `${differenceYear} year${differenceYear > 1 ? 's' : ''} ago` 
        }
        else if (differenceMonth > 0) {
            return `${differenceMonth} month${differenceMonth > 1 ? 's' : ''} ago` 
        } else if (differenceDay > 0) {
            return `${differenceDay} day${differenceDay > 1 ? 's' : ''} ago` 
        } else if (differenceHour > 0) {
            return `${differenceHour} hour${differenceHour > 1 ? 's' : ''} ago` 
        } else if (differenceMin > 0) {
            return `${differenceMin} minute${differenceMin > 1 ? 's' : ''} ago` 
        } else {
            return 'Just now' 
        }
    }

    return { formatTimeDifference }
}