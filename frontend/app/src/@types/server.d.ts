export interface ServerData {
    id: string;
    name: string;
    description: string;
    icon: string;
    category: string;
    channel_server: {
        id: string;
        name: string;
        server: string;
        topic: string;
        owner: string;
    }[];
}
