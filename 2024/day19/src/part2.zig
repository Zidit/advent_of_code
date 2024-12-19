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
var cache: std.StringHashMap(u64) = undefined;

fn test_pattern(design: []const u8, towels: [][]const u8) !u64 {
    if (design.len == 0) {
        return 1;
    }

    if (cache.contains(design)) {
        return cache.get(design).?;
    }

    var possible_designs: u64 = 0;
    for (towels) |towel| {
        if (design.len >= towel.len and std.mem.eql(u8, design[0..towel.len], towel)) {
            possible_designs += try test_pattern(design[towel.len..], towels);
        }
    }

    try cache.put(try cache.allocator.dupe(u8, design), possible_designs);
    return possible_designs;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    cache = std.StringHashMap(u64).init(allocator);

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

    var total: u64 = 0;
    for (designs.items) |design| {
        const possible_designs: u64 = try test_pattern(design, towels);
        total += possible_designs;
        //std.debug.print("Testing: {s} - {d}\n", .{ design, possible_designs });
    }
    std.debug.print("{d}\n", .{total});
}
