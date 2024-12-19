const std = @import("std");

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

//var cache: std.AutoHashMap(Key, true) = undefined;
var cache: std.StringHashMap(bool) = undefined;

fn test_pattern(design: []const u8, towels: [][]const u8) !bool {
    if (design.len == 0) {
        return true;
    }

    if (cache.contains(design)) {
        return cache.get(design).?;
    }

    for (towels) |towel| {
        if (design.len >= towel.len and std.mem.eql(u8, design[0..towel.len], towel)) {
            const is_valid: bool = try test_pattern(design[towel.len..], towels);
            try cache.put(try cache.allocator.dupe(u8, design), is_valid);

            if (is_valid)
                return true;
        }
    }

    return false;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    cache = std.StringHashMap(bool).init(allocator);

    const input = try read_input("src/input.txt");
    //const input = try read_input("src/example.txt");

    var lines = std.mem.splitSequence(u8, input, "\r\n");

    const towels = try split_string(lines.next().?, ", ", allocator);
    _ = lines.next();

    var designs = std.ArrayList([]const u8).init(allocator);
    while (lines.next()) |line| {
        try designs.append(line);
    }

    //std.debug.print("towels: {s}\n", .{towels});
    //std.debug.print("designs:\n", .{});
    //for (designs.items) |design| {
    //    std.debug.print("  {s}\n", .{design});
    //}

    var total: u32 = 0;
    for (designs.items) |design| {
        //std.debug.print("Testing: {s}\n", .{design});
        if (try test_pattern(design, towels)) {
            total += 1;
            //std.debug.print("Match: {s}\n", .{design});
        }
    }
    std.debug.print("{d}\n", .{total});
}
