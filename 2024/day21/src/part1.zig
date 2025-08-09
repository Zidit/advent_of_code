const std = @import("std");

const invalid_path = error{
    invalid_path,
};

const Vec2 = struct {
    x: i32,
    y: i32,

    pub fn init(x: anytype, y: anytype) Vec2 {
        return .{ .x = @intCast(x), .y = @intCast(y) };
    }

    pub fn add(self: Vec2, other: Vec2) Vec2 {
        return .{ .x = self.x + other.x, .y = self.y + other.y };
    }

    pub fn equal(self: Vec2, other: Vec2) bool {
        return self.x == other.x and self.y == other.y;
    }
};

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn split_string(input: []const u8, delim: []const u8, allocator: std.mem.Allocator) ![][]const u8 {
    var arr = std.ArrayList([]const u8).init(allocator);
    defer arr.deinit();

    var parts = std.mem.splitSequence(u8, input, delim);
    while (parts.next()) |p| {
        try arr.append(p);
    }

    return arr.toOwnedSlice();
}

const numpad: [11]Vec2 = .{
    Vec2.init(1, 3), // 0
    Vec2.init(0, 2), // 1
    Vec2.init(1, 2), // 2
    Vec2.init(2, 2), // 3
    Vec2.init(0, 1), // 4
    Vec2.init(1, 1), // 5
    Vec2.init(2, 1), // 6
    Vec2.init(0, 0), // 7
    Vec2.init(1, 0), // 8
    Vec2.init(2, 0), // 9
    Vec2.init(2, 3), // A
};

const keypad: [5]Vec2 = .{
    Vec2.init(1, 0), // ^
    Vec2.init(2, 0), // A
    Vec2.init(0, 1), // <
    Vec2.init(1, 1), // v
    Vec2.init(2, 1), // >
};

fn num_moves_hv(start: usize, end: usize, allocator: std.mem.Allocator) ![]u8 {
    const start_vec = numpad[start];
    const end_vec = numpad[end];

    var dx: i32 = end_vec.x - start_vec.x;
    var dy: i32 = end_vec.y - start_vec.y;

    if (start_vec.y == 3 and end_vec.x == 0)
        return error.invalid_path;

    var ret = std.ArrayList(u8).init(allocator);

    while (dx < 0) : (dx += 1)
        try ret.append('<');

    while (dx > 0) : (dx -= 1)
        try ret.append('>');

    while (dy < 0) : (dy += 1)
        try ret.append('^');

    while (dy > 0) : (dy -= 1)
        try ret.append('v');

    try ret.append('A');

    return ret.toOwnedSlice();
}

fn num_moves_vh(start: usize, end: usize, allocator: std.mem.Allocator) ![]u8 {
    const start_vec = numpad[start];
    const end_vec = numpad[end];

    var dx: i32 = end_vec.x - start_vec.x;
    var dy: i32 = end_vec.y - start_vec.y;

    if (start_vec.x == 0 and end_vec.y == 3)
        return error.invalid_path;

    var ret = std.ArrayList(u8).init(allocator);

    while (dy < 0) : (dy += 1)
        try ret.append('^');

    while (dy > 0) : (dy -= 1)
        try ret.append('v');

    while (dx < 0) : (dx += 1)
        try ret.append('<');

    while (dx > 0) : (dx -= 1)
        try ret.append('>');

    try ret.append('A');

    return ret.toOwnedSlice();
}

fn key_move(start: u8, end: u8) []const u8 {
    if (start == 'A') {
        if (end == 'A')
            return "A";
        if (end == '^')
            return "<A";
        if (end == '>')
            return "vA";
        if (end == 'v')
            return "v<A";
        if (end == '<')
            return "v<<A";
    } else if (start == '^') {
        if (end == 'A')
            return ">A";
        if (end == '^')
            return "A";
        if (end == '>')
            return ">vA";
        if (end == 'v')
            return "vA";
        if (end == '<')
            return "v<A";
    } else if (start == '>') {
        if (end == 'A')
            return "^A";
        if (end == '^')
            return "^<A";
        if (end == '>')
            return "A";
        if (end == 'v')
            return "<A";
        if (end == '<')
            return "<<A";
    } else if (start == 'v') {
        if (end == 'A')
            return ">^A";
        if (end == '^')
            return "^A";
        if (end == '>')
            return ">A";
        if (end == 'v')
            return "A";
        if (end == '<')
            return "<A";
    } else if (start == '<') {
        if (end == 'A')
            return ">>^A";
        if (end == '^')
            return ">^A";
        if (end == '>')
            return ">>A";
        if (end == 'v')
            return ">A";
        if (end == '<')
            return "A";
    }

    return "";
}

fn key_moves_recursive(seq: []const u8, iterations: u32) u64 {
    if (iterations == 0)
        return 1;

    var move_count: u64 = 0;

    var start: u8 = 'A';
    for (seq) |p| {
        const moves = key_move(start, p);
        move_count += key_moves_recursive(moves, iterations - 1);
        start = p;
    }
    return move_count;
}

fn get_press_count(start: usize, end: usize, allocator: std.mem.Allocator) !usize {
    var sequneces = std.ArrayList([]u8).init(allocator);
    defer sequneces.deinit();

    // Get press seq with horizontal moves first
    if (num_moves_hv(start, end, allocator)) |hv| {
        try sequneces.append(hv);
    } else |_| {}

    // Get press seq with vertical moves first
    if (num_moves_vh(start, end, allocator)) |vh| {
        try sequneces.append(vh);
    } else |_| {}

    // Get the shorter seq of the two
    var shortest: usize = std.math.maxInt(usize);
    for (sequneces.items) |seq| {
        shortest = @min(shortest, key_moves_recursive(seq, 3));
    }

    return shortest;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    //cache = std.StringHashMap(bool).init(allocator);

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var total: usize = 0;
    var lines = std.mem.splitSequence(u8, input, "\r\n");
    while (lines.next()) |line| {
        var start_key: usize = 10;

        var total_presses: u64 = 0;

        for (line) |p1| {
            const s: [1]u8 = .{p1};
            const target_key = try std.fmt.parseInt(u8, &s, 16);

            total_presses += try get_press_count(start_key, target_key, allocator);
            start_key = target_key;
        }

        const num_part = try std.fmt.parseInt(usize, line[0..3], 10);
        //std.debug.print("{d},{d},{d}\n\n", .{ total_presses, num_part, total_presses * num_part });

        total += num_part * total_presses;
    }

    std.debug.print("{d}\n", .{total});
}
