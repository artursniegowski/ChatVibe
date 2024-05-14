export interface IuseServer {
    joinServer: (serverId: string) => Promise<void>;
    leaveServer: (serverId: string) => Promise<void>;
    isMember: (serverId: string) => Promise<void>;
    // state that we can share between multiple compoenent to check if 
    // a user is a member or not
    isUserMember: boolean;
    error: Error | null;
    isLoading: boolean;
}