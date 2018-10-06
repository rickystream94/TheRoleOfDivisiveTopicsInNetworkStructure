using Printf

function split_line(line::String)
    n1, n2, value = split(line, ",")
    key = join([n1, n2], ",")
    value = parse(Int8, value)
    return key, value
end

function compute_edge_periods(mmr_enc_with_period_fn::String)::Dict{String,AbstractArray{Int8,1}}
    edge_periods_dict = Dict{String,AbstractArray{Int8,1}}()
    lines = Int64(0)
    open(mmr_enc_with_period_fn) do input
        for line in eachline(input)
            if lines % 50000000 == 0
                @printf "Processed %d lines...\n" lines
            end
            key, value = split_line(line)
            if !haskey(edge_periods_dict, key)
                edge_periods_dict[key] = Array{Int8,1}()
            end
            push!(edge_periods_dict[key], value)
            lines += 1
            flush(stdout)
        end
    end
    println("Done!")
    return edge_periods_dict
end

function dump_mmr_to_file(mmr_final_filename::String, edge_periods_dict::Dict{String,AbstractArray{Int8,1}})
    println("Dumping final MMR to file...")
    flush(stdout)
    open(mmr_final_filename, "w") do output
        for key in keys(edge_periods_dict)
            write(output, join([key, join(edge_periods_dict[key], ";")], ",") * "\n")
        end
    end
    println("Done!")
    flush(stdout)
end

mmr_final_filename = String("../data/mmr_encoded_final.csv")
mmr_enc_with_period_fn = String("../data/mmr_encoded_with_period.csv")

@time edge_periods_dict = compute_edge_periods(mmr_enc_with_period_fn)
@time dump_mmr_to_file(mmr_final_filename, edge_periods_dict)