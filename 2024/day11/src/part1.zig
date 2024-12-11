const std = @import("std");

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn digits(v: u64) u64 {
    var c: usize = 1;
    var t: u64 = v;
    while (t >= 10) {
        t /= 10;
        c += 1;
    }

    return c;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var cur_state = std.ArrayList(u64).init(allocator);
    var next_state = std.ArrayList(u64).init(allocator);

    var values = std.mem.splitSequence(u8, input, " ");
    while (values.next()) |v| {
        try cur_state.append(try std.fmt.parseInt(u64, v, 10));
    }

    for (0..25) |_| {
        for (cur_state.items) |v| {
            if (v == 0) {
                try next_state.append(1);
                continue;
            }

            const d = digits(v);
            if (d % 2 == 0) {
                const a: u64 = v / std.math.pow(u64, 10, d / 2);
                const b: u64 = v % std.math.pow(u64, 10, d / 2);
                try next_state.append(a);
                try next_state.append(b);
            } else {
                try next_state.append(v * 2024);
            }
        }

        cur_state = next_state;
        //std.debug.print("State: {any}\n", .{next_state.items});

        next_state = std.ArrayList(u64).init(allocator);

        //try next_state.append(0);
    }

    std.debug.print("{d}\n", .{cur_state.items.len});
}
