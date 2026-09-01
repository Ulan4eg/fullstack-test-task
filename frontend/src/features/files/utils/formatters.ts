import {kiloByteSize, megaByteSize} from "@/shared/constants";

export const formatters = {
    date: (value: string) => {
        return new Intl.DateTimeFormat('ru-RU', {
            dateStyle: 'short',
            timeStyle: 'short',
        }).format(new Date(value));
    },

    fileSize: (size: number) => {
        if (size < kiloByteSize) return `${size} B`;
        if (size < megaByteSize) return `${(size / kiloByteSize).toFixed(1)} KB`;
        return `${(size / megaByteSize).toFixed(1)} MB`;
    },


};