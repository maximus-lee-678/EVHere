import { DateTime } from 'luxon';

// Formats an ISO date for display. Format defaults to 'DD h:mma'.
// Tokens: https://moment.github.io/luxon/#/formatting?id=table-of-tokens
export function FormatDateTime(InputDateTime, FormatString = 'DD h:mma') {
    return DateTime
        .fromISO(InputDateTime)
        .toFormat(FormatString);
}

// Calculates the difference between 2 ISO times. Format defaults to hours and minutes.
// Formats: ['years', 'months', 'days', 'hours', 'minutes', 'seconds', 'milliseconds']
export function GetDateDiffString(DateTimeStart, DateTimeEnd, TimeStepsArray = ['hours', 'minutes']) {
    const End = DateTime.fromISO(DateTimeEnd);
    const Start = DateTime.fromISO(DateTimeStart);

    const DiffObj = End.diff(Start,
        TimeStepsArray)
        .toObject();

    let ReturnString = "";
    for (var key of TimeStepsArray) {
        ReturnString = ReturnString.concat(`${Math.floor(DiffObj[key])} ${key}, `);
    }
    ReturnString = ReturnString.slice(0, -2);

    return ReturnString;
}
