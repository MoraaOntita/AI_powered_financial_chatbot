export function formatCurrency(amount) {
    return `$${amount.toFixed(2)}`;
}

export function formatDate(date) {
    return new Intl.DateTimeFormat('en-US').format(new Date(date));
}
