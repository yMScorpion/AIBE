import { create } from "zustand";
import { api, type MeetingResponse } from "@/lib/api";

interface MeetingState {
  meetings: MeetingResponse[];
  loading: boolean;
  refreshMeetings: () => Promise<void>;
}

export const useMeetingStore = create<MeetingState>((set) => ({
  meetings: [],
  loading: false,
  refreshMeetings: async () => {
    set({ loading: true });
    try {
      const data = await api.meetings.list();
      set({ meetings: data.meetings });
    } catch {
      set({ meetings: [] });
    } finally {
      set({ loading: false });
    }
  },
}));
