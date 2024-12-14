const std = @import("std");

const Map = struct { data: []u8, h: usize, w: usize };

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

fn read_input(file_name: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_name, .{});
    defer file.close();

    var buffer: [1024 * 1024]u8 = undefined;
    const len = try file.readAll(&buffer);

    return buffer[0..len];
}

fn split_srting(input: []const u8, delim: u8, allocator: std.mem.Allocator) ![][]const u8 {
    var arr = std.ArrayList([]const u8).init(allocator);
    defer arr.deinit();

    var parts = std.mem.splitScalar(u8, input, delim);
    while (parts.next()) |p| {
        try arr.append(p);
    }

    return arr.toOwnedSlice();
}

fn map_inc(map: Map, pos: Vec2) !void {
    if (pos.x < 0 or pos.y < 0 or pos.y >= map.h or pos.x >= map.w)
        return error.OutOfRange;

    const x: usize = @intCast(pos.x);
    const y: usize = @intCast(pos.y);
    map.data[y * map.w + x] += 1;
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

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    const sec = 100;
    const width = 101;
    const height = 103;

    const map_data = try allocator.alloc(u8, width * height);
    @memset(map_data, 0);
    const map: Map = .{ .data = map_data, .h = height, .w = width };
    defer allocator.free(map_data);

    var end_pos = std.ArrayList(Vec2).init(allocator);
    defer end_pos.deinit();

    var lines = std.mem.splitSequence(u8, input, "\n");
    while (lines.next()) |line| {
        const line_trim = std.mem.trim(u8, line, " \n\r");
        const pv = try split_srting(line_trim, ' ', allocator);

        const p = try split_srting((try split_srting(pv[0], '=', allocator))[1], ',', allocator);
        const pos = Vec2.init(try std.fmt.parseInt(i32, p[0], 10), try std.fmt.parseInt(i32, p[1], 10));

        const v = try split_srting((try split_srting(pv[1], '=', allocator))[1], ',', allocator);
        const vel = Vec2.init(try std.fmt.parseInt(i32, v[0], 10), try std.fmt.parseInt(i32, v[1], 10));

        //std.debug.print("{any}, {any}\n", .{ pos, vel });

        var end = Vec2.init(pos.x + vel.x * sec, pos.y + vel.y * sec);
        end = Vec2.init(@rem(end.x, width), @rem(end.y, height));
        end = Vec2.init(if (end.x < 0) width + end.x else end.x, if (end.y < 0) height + end.y else end.y);

        try end_pos.append(end);
        //std.debug.print("{any}\n", .{end});
        try map_inc(map, end);
    }

    //print_map_d(map);

    var q1: u32 = 0;
    var q2: u32 = 0;
    var q3: u32 = 0;
    var q4: u32 = 0;

    const ws = @divFloor(width, 2);
    const hs = @divFloor(height, 2);

    for (end_pos.items) |p| {
        if (p.x < ws and p.y < hs) {
            q1 += 1;
        } else if (p.x > ws and p.y < hs) {
            q2 += 1;
        } else if (p.x < ws and p.y > hs) {
            q3 += 1;
        } else if (p.x > ws and p.y > hs) {
            q4 += 1;
        } else {
            //std.debug.print("err", .{});
        }
    }

    const total = q1 * q2 * q3 * q4;
    std.debug.print("{d}\n", .{total});
}
