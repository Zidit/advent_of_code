const std = @import("std");

const Vec2 = struct {
    x: i32,
    y: i32,

    pub fn init(x: i32, y: i32) Vec2 {
        return .{ .x = x, .y = y };
    }

    pub fn init_u(x: u32, y: u32) Vec2 {
        return .{ .x = @intCast(x), .y = @intCast(y) };
    }

    pub fn add(self: Vec2, other: Vec2) Vec2 {
        return .{ .x = self.x + other.x, .y = self.y + other.y };
    }

    pub fn equal(self: Vec2, other: Vec2) bool {
        return self.x == other.x and self.y == other.y;
    }
};
const Map = struct { data: []u8, h: usize, w: usize, allocator: std.mem.Allocator };

const neighbors = [_]Vec2{
    .{ .x = 0, .y = -1 }, //Up
    .{ .x = 1, .y = 0 }, //Right
    .{ .x = 0, .y = 1 }, //Down
    .{ .x = -1, .y = 0 }, //Left
};

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn map_set(map: Map, pos: Vec2, c: u8) void {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    map.data[y * map.w + x] = c;
}

fn map_get(map: Map, pos: Vec2) ?u8 {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return null;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    return map.data[y * map.w + x];
}

fn map_inc(map: Map, pos: Vec2) !void {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return error.OutOfRange;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    map.data[y * map.w + x] += 1;
}

fn print_map(map: Map) void {
    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        std.debug.print("{s}\n", .{line});
    }
    std.debug.print("\n", .{});
    return;
}

fn print_map_d(map: Map) void {
    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        for (line) |value| {
            std.debug.print("{d} ", .{value});
        }
        std.debug.print("\n", .{});
    }
    std.debug.print("\n", .{});
    return;
}

fn find_from_map(map: Map, needle: u8, allocator: std.mem.Allocator) ![]Vec2 {
    var results = std.ArrayList(Vec2).init(allocator);
    defer results.deinit();

    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        var pos: usize = 0;

        while (std.mem.indexOfScalarPos(
            u8,
            line,
            pos,
            needle,
        )) |index| {
            try results.append(.{ .x = @intCast(index), .y = @intCast(y) });
            pos = index + 1;
        }
    }

    return results.toOwnedSlice();
}

fn find_uniques_from_map(map: Map, allocator: std.mem.Allocator) std.AutoHashMap(u8, Vec2) {
    var results = std.AutoHashMap(u8, Vec2).init(allocator);

    for (0..map.h) |y| {
        const line = map.data[y * map.w .. (y + 1) * map.w];
        for (0..map.w) |x| {
            if (!results.contains(line[x])) {
                try results.put(line[x], .{ .x = x, .y = y });
            }
        }
    }

    return results;
}

fn data_to_map(input: []const u8, allocator: std.mem.Allocator) !Map {
    var data = std.ArrayList(u8).init(allocator);
    var height: usize = 0;
    var width: usize = 0;

    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        if (width == 0) {
            width = line_trimmed.len;
        } else if (width != line_trimmed.len) {
            return error.OutOfRange;
        }

        try data.appendSlice(line_trimmed);
        height += 1;
    }

    return .{ .data = try data.toOwnedSlice(), .h = height, .w = width, .allocator = allocator };
}

fn deinit_map(map: Map) void {
    map.allocator.free(map.data);
}

fn can_move(map: Map, pos: Vec2, dir: Vec2) bool {
    const next = pos.add(dir);
    const c = map_get(map, next).?;
    if (c == '#')
        return false;
    if (c == '.')
        return true;

    var next2: Vec2 = next;
    if (c == '[')
        next2.x += 1;
    if (c == ']')
        next2.x += -1;

    return can_move(map, next, dir) and can_move(map, next2, dir);
}

fn move_step(map: Map, pos: Vec2, dir: Vec2) void {
    const next = pos.add(dir);
    const cur_c = map_get(map, pos).?;
    const next_c = map_get(map, next).?;

    if (next_c == '[') {
        const next2 = Vec2.init(next.x + 1, next.y);
        move_step(map, next, dir);
        move_step(map, next2, dir);
    } else if (next_c == ']') {
        const next2 = Vec2.init(next.x - 1, next.y);
        move_step(map, next, dir);
        move_step(map, next2, dir);
    }

    map_set(map, next, cur_c);
    map_set(map, pos, '.');
    return;
}

fn move_vert(map: Map, pos: Vec2, dir: Vec2) Vec2 {
    if (!can_move(map, pos, dir))
        return pos;

    move_step(map, pos, dir);
    return pos.add(dir);
}

fn move_hor(map: Map, pos: Vec2, dir: Vec2) Vec2 {
    var next = pos;
    while (true) {
        next = next.add(dir);
        const c = map_get(map, next).?;
        if (c == '#')
            return pos;
        if (c == '.')
            break;
    }

    const dir_b = Vec2.init(dir.x * -1, dir.y * -1);
    var prev = next.add(dir_b);
    while (!Vec2.equal(pos, next)) {
        map_set(map, next, map_get(map, prev).?);
        prev = prev.add(dir_b);
        next = next.add(dir_b);
    }

    map_set(map, pos, '.');
    return pos.add(dir);
}

fn move(map: Map, pos: Vec2, dir: Vec2) Vec2 {
    if (dir.x != 0) {
        return move_hor(map, pos, dir);
    } else {
        return move_vert(map, pos, dir);
    }
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var parts = std.mem.splitSequence(u8, input, "\r\n\r\n");
    var map = try data_to_map(parts.next().?, allocator);
    defer deinit_map(map);
    print_map(map);

    var instructions = std.ArrayList(u8).init(allocator);
    var lines = std.mem.splitSequence(u8, parts.next().?, "\n");
    while (lines.next()) |line| {
        const line_trimmed = std.mem.trim(u8, line, " \n\r");
        try instructions.appendSlice(line_trimmed);
    }

    //Widen map
    var wide_data = std.ArrayList(u8).init(allocator);
    defer wide_data.deinit();

    for (map.data) |c| {
        if (c == '#')
            try wide_data.appendSlice("##");
        if (c == 'O')
            try wide_data.appendSlice("[]");
        if (c == '.')
            try wide_data.appendSlice("..");
        if (c == '@')
            try wide_data.appendSlice("@.");
    }

    const map_new: Map = .{ .data = try wide_data.toOwnedSlice(), .w = map.w * 2, .h = map.h, .allocator = map.allocator };
    defer deinit_map(map_new);

    map = map_new;
    print_map(map);

    //std.debug.print("{s}\n", .{instructions.items});

    var pos: Vec2 = (try find_from_map(map, '@', allocator))[0];

    for (instructions.items) |i| {
        //std.debug.print("Move {c}:\n", .{i});

        switch (i) {
            '^' => {
                pos = move(map, pos, neighbors[0]);
            },
            '>' => {
                pos = move(map, pos, neighbors[1]);
            },
            'v' => {
                pos = move(map, pos, neighbors[2]);
            },
            '<' => {
                pos = move(map, pos, neighbors[3]);
            },
            else => {
                std.debug.print("err\n", .{});
            },
        }

        //print_map(map);
    }

    var total: u32 = 0;
    for (try find_from_map(map, '[', allocator)) |box| {
        const x: u32 = @intCast(box.x);
        const y: u32 = @intCast(box.y);
        total += y * 100 + x;
    }

    std.debug.print("{d}\n", .{total});
}
